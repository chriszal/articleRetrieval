from assets.database import Database
class User(object):
    def __init__(self):
        self.collection_name = 'user'  # collection name
        self.db = Database()
        self.fields = {
            "keywords": "list",
            "email": "string",
            "created": "datetime",
            "city": "string",
        }

        self.create_required_fields = ["email"]

    def create(self, user):
        # Validator will throw error if invalid
        res = self.db.insert_user(user, self.collection_name)
        return res

    def find(self, user):  # find_user all
        return self.db.find_user(user, self.collection_name)

    def find_by_email(self, email):
        return self.db.find_by_id(email, self.collection_name)

    def update(self, email, user):
        return self.db.update_user(email, user, self.collection_name)

    def delete(self, email):
        return self.db.delete_user(email, self.collection_name)
