import datetime

from models.db_settings import get_db


class Message:
    """
    Message schema:
    - message (string)
    """

    @classmethod
    def create(cls, text):
        db = get_db()
        messages_ref = db.collection(u'messages')  # a reference to the messages collection

        message_ref = messages_ref.document()  # create a message document reference
        # now you can create or update the message document (set: if it exists, update it. If not, create a new one).
        message_ref.set({
            u'text': u'{}'.format(text),  # we could also name this smth else, like "text", to avoid confusion
            u'created': datetime.datetime.now(),
            # you could add other fields here, like "author", "email" etc.
        })

        # create message dict
        message_dict = message_ref.get().to_dict()
        message_dict["id"] = message_ref.id  # add ID to the message dict (because it's not added automatically)

        return message_dict

    @classmethod
    def fetch_all(cls):
        db = get_db()
        messages_ref = db.collection(u'messages')  # a reference to the messages collection

        # messages generator: holds all message documents (these documents need to be converted to dicts)
        messages_gen = messages_ref.stream()

        messages = []
        for message in messages_gen:
            message_dict = message.to_dict()  # converting DocumentSnapshot into a dictionary

            message_dict["id"] = message.id  # adding message ID to the dict, because it's not there by default
            messages.append(message_dict)  # appending the message dict to the messages list

        return messages
