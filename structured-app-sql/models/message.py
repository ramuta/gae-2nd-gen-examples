from models.db_settings import get_db

db = get_db()


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Message %r>' % self.title

    @classmethod
    def create(cls, text):
        message = Message(text=text)
        db.add(message)
        db.commit()

        return message

    @classmethod
    def fetch_all(cls):
        messages = db.query(Message).all()

        return messages


# this is needed to create the table in the database
db.create_all()
