import os
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    name = "SmartNinja 2 :)"
    return render_template("index.html", name=name)


if __name__ == '__main__':
    if os.getenv('GAE_ENV', '').startswith('standard'):
        app.run()  # production
    else:
        app.run(port=8080, host="localhost")  # localhost
