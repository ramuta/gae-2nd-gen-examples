import os
import mock
from google.cloud import firestore
import google.auth.credentials


def get_db():
    # config database
    if os.getenv('GAE_ENV', '').startswith('standard'):
        # production
        db = firestore.Client()
    else:
        # localhost
        os.environ["FIRESTORE_DATASET"] = "test"
        os.environ["FIRESTORE_PROJECT_ID"] = "test"

        if os.getenv('TESTING', '').startswith('yes'):
            os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8002"
            os.environ["FIRESTORE_EMULATOR_HOST_PATH"] = "localhost:8002/firestore"
            os.environ["FIRESTORE_HOST"] = "http://localhost:8002"
        else:
            os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8001"
            os.environ["FIRESTORE_EMULATOR_HOST_PATH"] = "localhost:8001/firestore"
            os.environ["FIRESTORE_HOST"] = "http://localhost:8001"

        credentials = mock.Mock(spec=google.auth.credentials.Credentials)
        db = firestore.Client(project="test", credentials=credentials)

    return db
