import os

from flask import render_template, request, redirect, url_for, abort, make_response

from models.user import User
from utils.decorators import public_handler


@public_handler
def index(**params):
    return render_template("public/index.html", **params)


@public_handler
def login(**params):
    if request.method == "GET":
        return render_template("public/login.html", **params)

    elif request.method == "POST":
        username = request.form.get("login-username")
        password = request.form.get("login-password")

        if username and password:
            # find a User with this username (if it doesn't exist: 404)
            user = User.get_by_username(username=username)

            if not user:
                return abort(404)

            # check if passwords match (if not: 403)
            if User.is_password_valid(user=user, password=password):
                # if passwords match, generate a session token and save its hash in the database
                session_token = User.generate_session_token(user=user, request=request)

                # prepare a response and then store the token in a cookie
                response = make_response(redirect(url_for("profile.main")))

                # on localhost don't make the cookie secure and http-only (but on production it should be)
                cookie_secure_httponly = False
                if os.getenv('GAE_ENV', '').startswith('standard'):
                    cookie_secure_httponly = True

                # store the token in a cookie
                response.set_cookie(key="my-web-app-session", value=session_token, secure=cookie_secure_httponly,
                                    httponly=cookie_secure_httponly)
                return response

        return abort(403)


@public_handler
def registration(**params):
    if request.method == "GET":
        return render_template("public/registration.html", **params)

    elif request.method == "POST":
        username = request.form.get("registration-username")
        password = request.form.get("registration-password")
        repeat = request.form.get("registration-repeat")

        if username and password and password == repeat:
            # check if there's any admin yet
            if User.is_there_any_admin():
                set_admin = False
            else:  # if there's not, set the first registered user as an admin
                set_admin = True

            user = User.create(username=username, password=password, admin=set_admin)

            if user:
                return render_template("public/registration-success.html", **params)
            else:
                return abort(403, description="This username is not available!")
