from google.cloud import ndb
from models.db_settings import get_db

client = get_db()


class Message(ndb.Model):
    text = ndb.StringProperty()

    @classmethod
    def create(cls, text):
        with client.context():  # with client.context() is obligatory to use in the new ndb library
            message = cls(text=text)
            message.put()

            return message

    @classmethod
    def fetch_all(cls):
        with client.context():
            messages = cls.query().fetch()
            return messages
