import os
from sqla_wrapper import SQLAlchemy


def get_db():
    # determine the database URL
    db_user = os.environ.get('CLOUD_SQL_USERNAME')
    db_password = os.environ.get('CLOUD_SQL_PASSWORD')
    db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
    db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

    if db_user and db_password and db_name and db_connection_name:  # if on google cloud, connect to PostgreSQL
        sqla_db_uri = f"postgresql://{db_user}:{db_password}@/{db_name}?host=/cloudsql/{db_connection_name}"
    else:  # if on localhost, use SQLite
        if os.getenv('TESTING', '').startswith('yes'):
            sqla_db_uri = "sqlite:///:memory:"
        else:
            sqla_db_uri = "sqlite:///localhost.sqlite"

    db = SQLAlchemy(sqla_db_uri)

    return db
