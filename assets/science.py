from assets.database import Database

class Science(object):
    def __init__(self):
        self.collection_name = 'science'  # collection name
        self.db = Database()
        self.fields = {
            "source": {
                "id": "string",
                "name": "string"
            },
            "author": "string",
            "title": "string",
            "description": "string",
            "url": "string",
            "urlToImage": "string",
            "publishedAt": "datetime",
            "content": "string"
        }

    def find_all(self):  # find_user all
        return self.db.find_articles(self.collection_name)