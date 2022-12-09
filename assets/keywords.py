from assets.database import Database

class Keywords(object):
    def __init__(self):
        self.collection_name = 'keywords'
        self.db = Database()
        self.fields = {
            "agriculture": "object",
            "business": "object",
            "health": "object",
            "space": "object",
            "science": "object",
            "tech": "object",
            "war": "object",
            "motosport": "object",
        }

    def create(self, articles):

        res = self.db.insert_article(articles, self.collection_name)
        return res

    def find_all(self):  # find_user all
        return self.db.find_articles(self.collection_name)

