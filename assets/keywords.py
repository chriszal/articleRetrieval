from assets.database import Database

class Keywords(object):
    def __init__(self):
        self.collection_name = 'keywords'
        self.db = Database()
        self.fields = {
            "agriculture": "object",
            "business": "object",
            "elon": "object",
            "space": "object",
            "science": "object",
            "tech": "object",
            "war": "object",
            "motosport": "object",
        }

    def find_all(self):  # find_user all
        return self.db.find_articles(self.collection_name)

