from assets.database import Database

class SourceDomainDescriptions(object):
    def __init__(self):
        self.collection_name = 'source domain name'  # collection name
        self.db = Database()
        self.fields = {
            "source": {
                "id": "string",
                "name": "string"
            },
            "description": "string"
        }

    def fetch_domain_descriptionzç(self):  # find_user all
        return self.db.find_articles(self.collection_name)
