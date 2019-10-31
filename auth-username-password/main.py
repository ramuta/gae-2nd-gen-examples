import os
from flask import Flask
from handlers import public, admin, profile

app = Flask(__name__)

# URL ROUTES:

# public
app.add_url_rule(rule="/", endpoint="public.index", view_func=public.index, methods=["GET"])
app.add_url_rule(rule="/login", endpoint="public.login", view_func=public.login, methods=["GET", "POST"])
app.add_url_rule(rule="/registration", endpoint="public.registration", view_func=public.registration,
                 methods=["GET", "POST"])

# profile
app.add_url_rule(rule="/profile", endpoint="profile.main", view_func=profile.main, methods=["GET"])
app.add_url_rule(rule="/profile/session/delete", endpoint="profile.session_delete", view_func=profile.session_delete,
                 methods=["POST"])

# admin
app.add_url_rule(rule="/admin", endpoint="admin.main", view_func=admin.main, methods=["GET"])


if __name__ == '__main__':
    if os.getenv('GAE_ENV', '').startswith('standard'):
        app.run()  # production
    else:
        app.run(port=8080, host="localhost", debug=True)  # localhost
