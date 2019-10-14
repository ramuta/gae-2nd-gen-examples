import os
from google.cloud import ndb
import google.auth.credentials
import mock


def get_db():
    if os.getenv('GAE_ENV', '').startswith('standard'):
        # production
        db = ndb.Client()
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
        db = ndb.Client(project="test", credentials=credentials)

    return db
