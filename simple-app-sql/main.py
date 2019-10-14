import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# determine the database URL
db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

if db_user and db_password and db_name and db_connection_name:  # if on google cloud, connect to PostgreSQL
    sqla_db_uri = f"postgresql://{db_user}:{db_password}@/{db_name}?host=/cloudsql/{db_connection_name}"
else:  # if on localhost, use SQLite
    sqla_db_uri = "sqlite:///localhost.sqlite"

app.config['SQLALCHEMY_DATABASE_URI'] = sqla_db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Message %r>' % self.title


# create all tables in the database
db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    # get all messages from the db
    messages = db.session.query(Message).all()

    if request.method == "POST":
        # create a new message
        message = Message(text=request.form.get("message"))
        db.session.add(message)
        db.session.commit()

    return render_template("index.html", messages=messages)


if __name__ == '__main__':
    if os.getenv('GAE_ENV', '').startswith('standard'):
        app.run()  # production
    else:
        app.run(port=8080, host="localhost")  # localhost
