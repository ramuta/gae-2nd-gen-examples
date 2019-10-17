import datetime
import os

import mock
from flask import Flask, render_template, request
from google.cloud import datastore
import google.auth.credentials

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    # config database
    if os.getenv('GAE_ENV', '').startswith('standard'):
        # production
        db = datastore.Client()
    else:
        # localhost
        os.environ["DATASTORE_DATASET"] = "test"
        os.environ["DATASTORE_PROJECT_ID"] = "test"

        if os.getenv('TESTING', '').startswith('yes'):
            os.environ["DATASTORE_EMULATOR_HOST"] = "localhost:8002"
            os.environ["DATASTORE_EMULATOR_HOST_PATH"] = "localhost:8002/datastore"
            os.environ["DATASTORE_HOST"] = "http://localhost:8002"
        else:
            os.environ["DATASTORE_EMULATOR_HOST"] = "localhost:8001"
            os.environ["DATASTORE_EMULATOR_HOST_PATH"] = "localhost:8001/datastore"
            os.environ["DATASTORE_HOST"] = "http://localhost:8001"

        credentials = mock.Mock(spec=google.auth.credentials.Credentials)
        db = datastore.Client(project="test", credentials=credentials)

    # get all messages from the Datastore
    messages = db.query(kind='Message').fetch()

    if request.method == "POST":
        # add message to Datastore
        entity = datastore.Entity(key=db.key("Message"))

        # message model
        message = {
            "text": request.form.get("message"),
            "created": datetime.datetime.now(),
            # you could add other fields here, like "author", "email" etc.
        }

        entity.update(message)
        db.put(entity)

    return render_template("index.html", messages=messages)


@app.route("/basic", methods=["GET"])
def basic():
    return "Basic handler without HTML template"


if __name__ == '__main__':
    if os.getenv('GAE_ENV', '').startswith('standard'):
        app.run()  # production
    else:
        app.run(port=8080, host="localhost")  # localhost
