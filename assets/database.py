from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId


class Database(object):
    def __init__(self):
        self.client = MongoClient(host='mongodb_container',
                         port=27017,
                         username='',
                         password='')
        self.db = self.client["articles_keywords_db"]  #configure db name

    # User functions
    def insert_user(self, element, collection_name):
        existing_document = self.db[collection_name].find_one({"email":element["email"]})
        if not existing_document:
            element["created"] = datetime.now()
            inserted = self.db[collection_name].insert_one(element)  # insert_user data to db
            return "Inserted ID "+str(inserted.inserted_id)
        else:
            return "Email already used"
    def find_user(self, criteria, collection_name, projection=None, sort=None, limit=0, cursor=False):  # find_user all from db

        if "_id" in criteria:
            criteria["_id"] = ObjectId(criteria["_id"])

        found = self.db[collection_name].find(filter=criteria, projection=projection, limit=limit, sort=sort)

        if cursor:
            return found

        found = list(found)

        for i in range(len(found)):  # to serialize object id need to convert string
            if "_id" in found[i]:
                found[i]["_id"] = str(found[i]["_id"])

        return found
    def find_by_email(self, email, collection_name):
        found = self.db[collection_name].find_one({"email":email})
        
        if found is None:
            return not found
        
        # if "email" in found:
        #      found["email"] = str(found["email"])

        return found
    def update_user(self, email, element, collection_name):
        criteria = {"email":email}

        set_obj = {"$set": element}  # update_user value

        updated = self.db[collection_name].update_one(criteria, set_obj)
        if updated.matched_count == 1:
            return "Record Successfully Updated"
    def delete_user(self, email, collection_name):
        deleted = self.db[collection_name].delete_one({"email":email})
        return bool(deleted.deleted_count)

    # Keyword functions
    def find_articles(self, collection_name, limit=0): ##TODO -possible bug :)
        return self.db[collection_name].find(limit=limit)

    def insert_article(self, element, collection_name):
        
        inserted = self.db[collection_name].insert_one(element)  # insert_user data to db
            


