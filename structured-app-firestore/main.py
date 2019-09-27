import os
from flask import Flask
from handlers import public

app = Flask(__name__)

# URLs
app.add_url_rule(rule="/", endpoint="index", view_func=public.index, methods=["GET", "POST"])
app.add_url_rule(rule="/test", endpoint="test", view_func=public.test, methods=["GET"])


if __name__ == '__main__':
    if os.getenv('GAE_ENV', '').startswith('standard'):
        app.run()  # production
    else:
        app.run(port=8080, host="localhost", debug=True)  # localhost
