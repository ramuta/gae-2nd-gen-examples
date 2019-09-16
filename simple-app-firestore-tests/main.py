import os

import mock
from flask import Flask, render_template, request
from google.cloud import firestore
import google.auth.credentials


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    # config database
    if os.getenv('GAE_ENV', '').startswith('standard'):
        # production
        db = firestore.Client()
    else:
        # localhost
        os.environ["FIRESTORE_DATASET"] = "test"
        os.environ["FIRESTORE_PROJECT_ID"] = "test"

        if app.config['TESTING']:
            os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8002"
            os.environ["FIRESTORE_EMULATOR_HOST_PATH"] = "localhost:8002/firestore"
            os.environ["FIRESTORE_HOST"] = "http://localhost:8002"
        else:
            os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8001"
            os.environ["FIRESTORE_EMULATOR_HOST_PATH"] = "localhost:8001/firestore"
            os.environ["FIRESTORE_HOST"] = "http://localhost:8001"

        credentials = mock.Mock(spec=google.auth.credentials.Credentials)
        db = firestore.Client(project="test", credentials=credentials)

    # get all messages from the Firestore
    messages_ref = db.collection(u'messages')  # a reference to the messages collection
    messages_gen = messages_ref.stream()  # messages generator: holds all message documents (these documents need to be converted to dicts)

    messages = []
    for message in messages_gen:
        message_dict = message.to_dict()  # converting a message document into dict
        message_dict["id"] = message.id  # adding message ID to the dict, because it's not there by default
        messages.append(message_dict)  # appending the message dict to the messages list

    if request.method == "POST":
        # add message to Firestore
        message_ref = messages_ref.document()  # create a message document reference
        # now you can create or update the message document (set: if it exists, update it. If not, create a new one).
        message_ref.set({
            u'message': u'{}'.format(request.form.get("message")),
        })

    return render_template("index.html", messages=messages)


@app.route("/test", methods=["GET"])
def test():
    return "test"


if __name__ == '__main__':
    if os.getenv('GAE_ENV', '').startswith('standard'):
        app.run()  # production
    else:
        app.run(port=8080, host="localhost", debug=True)  # localhost
