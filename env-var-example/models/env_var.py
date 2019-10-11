import logging
from models.db_settings import get_db


class EnvVar:
    """
    EnvVar schema:
    - name
    - value
    """
    @classmethod
    def get(cls, name):
        db = get_db()

        col_ref = db.collection(u'envvars')  # a reference to the vars collection
        env_var_ref = col_ref.document(u"{}".format(name.upper()))  # get the env var document

        try:
            env_var = env_var_ref.get()
            env_var_dict = env_var.to_dict()  # convert env var document to dictionary
            env_var_dict["id"] = env_var.id  # add ID to the dictionary

            return env_var_dict
        except Exception as e:
            logging.warning(e)
            return None

    @classmethod
    def create(cls, name, value):
        db = get_db()
        col_ref = db.collection(u'envvars')  # a reference to the vars collection

        env_var_ref = col_ref.document(u"{}".format(name.upper()))  # create an env var document reference
        # now you can create or update the env var document (set: if it exists, update it. If not, create a new one).
        env_var_ref.set({
            u'name': u'{}'.format(name.upper()),  # env vars should be always uppercase
            u'value': u'{}'.format(value),
        })

        # create env var dict
        env_var_dict = env_var_ref.get().to_dict()
        env_var_dict["id"] = env_var_ref.id  # add ID to the env var dict (because it's not added automatically)

        return env_var_dict

    @classmethod
    def fetch_all(cls):
        db = get_db()

        col_ref = db.collection(u'envvars')  # a reference to the vars collection

        # collection generator: holds all env var documents (these documents need to be converted to dicts)
        col_gen = col_ref.stream()

        env_vars = []
        for env_var in col_gen:
            env_var_dict = env_var.to_dict()  # converting DocumentSnapshot into a dictionary

            env_var_dict["id"] = env_var.id  # adding env var ID to the dict, because it's not there by default
            env_vars.append(env_var_dict)  # appending the env var dict to the env vars list

        return env_vars
