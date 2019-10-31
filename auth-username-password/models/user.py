import datetime
import hashlib
import secrets

import bcrypt
from operator import attrgetter
from google.cloud import ndb
from models.db_settings import get_db

client = get_db()


class Session(ndb.Model):
    token_hash = ndb.StringProperty()
    ip = ndb.StringProperty()
    platform = ndb.StringProperty()
    browser = ndb.StringProperty()
    city = ndb.StringProperty()
    country = ndb.StringProperty()
    user_agent = ndb.StringProperty()
    expired = ndb.DateTimeProperty()


class CSRFToken(ndb.Model):
    """CSRF token (also called XSRF) is a mechanism that prevents CSRF attacks."""
    token = ndb.StringProperty()
    expired = ndb.DateTimeProperty()


class User(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()

    username = ndb.StringProperty()
    password_hash = ndb.StringProperty()  # use bcrypt: http://zetcode.com/python/bcrypt/, rounds=12

    admin = ndb.BooleanProperty(default=False)
    sessions = ndb.StructuredProperty(Session, repeated=True)
    csrf_tokens = ndb.StructuredProperty(CSRFToken, repeated=True)  # there should be max 10 CSRF tokens stored

    # standard model fields
    created = ndb.DateTimeProperty(auto_now_add=True)  # use https://github.com/miguelgrinberg/Flask-Moment
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, username, password, admin=False):
        with client.context():
            user = cls.query(cls.username == username).get()  # check if there's any user with the same name already

            if not user:
                # use bcrypt to hash the password
                hashed = bcrypt.hashpw(password=str.encode(password), salt=bcrypt.gensalt(12))

                # create the user object and store it into Datastore
                user = cls(username=username, password_hash=hashed, admin=admin)
                user.put()

                return user
            else:
                return False

    @classmethod
    def get_by_username(cls, username):
        with client.context():
            user = cls.query(cls.username == username).get()
            return user

    @classmethod
    def get_by_session_token(cls, session_token):
        with client.context():
            token_hash = hashlib.sha256(str.encode(session_token)).hexdigest()

            user = cls.query(cls.sessions.token_hash == token_hash).get()

            if not user:
                return None

            for session in user.sessions:
                if session.token_hash == token_hash:
                    if session.expired > datetime.datetime.now():
                        return user

            return None

    @classmethod
    def is_password_valid(cls, user, password):
        if bcrypt.checkpw(password=str.encode(password), hashed_password=str.encode(user.password_hash)):
            return True
        else:
            return False

    @classmethod
    def is_there_any_admin(cls):
        with client.context():
            admin = cls.query(cls.admin == True, cls.deleted == False).get()

            if admin:
                return True
            else:
                return False

    @classmethod
    def generate_session_token(cls, user, request=None):
        with client.context():
            # generate session token and its hash
            token = secrets.token_hex()
            token_hash = hashlib.sha256(str.encode(token)).hexdigest()

            # create a session
            session = Session(token_hash=token_hash, expired=(datetime.datetime.now() + datetime.timedelta(days=30)))
            if request:  # this separation is needed for tests which don't have the access to "request" variable
                session.ip = request.access_route[-1]
                session.platform = request.user_agent.platform
                session.browser = request.user_agent.browser
                session.user_agent = request.user_agent.string
                session.country = request.headers.get("X-AppEngine-Country")
                session.city = request.headers.get("X-AppEngine-City")

            # store the session in the User model
            if not user.sessions:
                user.sessions = [session]
            else:
                user.sessions.append(session)

            user.put()

            return token

    @classmethod
    def delete_session(cls, user, token_hash_five_chars):
        with client.context():
            valid_sessions = []
            for session in user.sessions:
                # delete session that has token hash that starts with these 5 characters
                # (delete by not including in the new sessions list)
                if not session.token_hash.startswith(token_hash_five_chars):
                    valid_sessions.append(session)

            user.sessions = valid_sessions
            user.put()

        return user

    @classmethod
    def set_csrf_token(cls, user):
        with client.context():
            # first delete expired tokens from the CSRF tokens list in the user object
            valid_tokens = []
            for csrf in user.csrf_tokens:
                if csrf.expired > datetime.datetime.now():
                    valid_tokens.append(csrf)

            # check how many csrf tokens are still left in the User object (should be 10 or less)
            # if more than 10, delete the oldest one (with the closest expired date)
            if len(valid_tokens) >= 10:
                oldest_token = min(valid_tokens, key=attrgetter("expired"))
                valid_tokens.remove(oldest_token)

            # then create a new CSRF token and enter it in the tokens list
            token = secrets.token_hex()
            csrf_object = CSRFToken(token=token, expired=(datetime.datetime.now() + datetime.timedelta(hours=8)))
            valid_tokens.append(csrf_object)

            # finally, store the new tokens list back in the user model
            user.csrf_tokens = valid_tokens
            user.put()

            return token

    @classmethod
    def is_csrf_token_valid(cls, user, csrf_token):
        with client.context():
            token_validity = False

            unused_tokens = []
            for csrf in user.csrf_tokens:  # loop through user's CSRF tokens
                if csrf.token == csrf_token:  # if tokens match, set validity to True
                    token_validity = True
                else:
                    unused_tokens.append(csrf)  # if not, add CSRF token to the unused_tokens list

            if unused_tokens != user.csrf_tokens:
                user.csrf_tokens = unused_tokens
                user.put()

            return token_validity
