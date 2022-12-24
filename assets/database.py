import json
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId, json_util
from pymongo.errors import CollectionInvalid
import logging
from bson.json_util import dumps

class Database(object):

    TOPICS = ["education",
              "health",
              "business",
              "motorsport",
              "science",
              "space",
              "technology",
              "war"]

    def __init__(self):
        self.client = MongoClient(host='mongodb_container',
                                  port=27017,
                                  username='root',
                                  password='rootpass')

        self.db = self.client["articles_keywords_db"]  # configure db name

        try:
            # initializing the collections
            self.sourceDomainName = self.db.create_collection("sourceDomainName", check_exists=True, validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["source", "description"],
                    "properties": {
                        "source": {
                            "bsonType": "string",
                            "description": "Source name that we keep the description of it"
                        },
                        "description": {
                            "bsonType": "string",
                            "description": "The description from wikipedia about the source with the above name"
                        }
                    }
                }
            })
        except CollectionInvalid as ci:
            print(f"You probabli do not have the right access or the collection already exists {ci}")
        finally:
            self.sourceDomainName = self.db["sourceDomainName"]

        article_schema = {
            "bsonType": "object",
            "description": "This is the type of each entry it should go in to this array",
            "properties": {
                "article": {
                    "bsonType": "string",
                    "description": "The articles text from the newsAPI"
                },
                "source": {
                    "bsonType": "string",
                    "description": "The article's source fro where this text is coming from"
                }
            }
        }
        try:
            # self.keywords = self.db.create_collection("keywords", check_exists=True, validator={
            #     "$jsonSchema": {
            #         "bsonType": "object",
            #         "properties": {
            #             "keywords": {
            #                 "description": "The keywords/topics for every article",
            #                 "type": "object",
            #                 "properties": {
            #                     "education": {
            #                         "bsonType": "array",
            #                         "description": "Articles for education",
            #                         "items": article_schema
            #                     },
            #                     "health": {
            #                         "bsonType": "array",
            #                         "description": "Articles for health",
            #                         "items": article_schema
            #                     },
            #                     "business": {
            #                         "bsonType": "array",
            #                         "description": "Articles for bussiness",
            #                         "items": article_schema
            #                     },
            #                     "motorsport": {
            #                         "bsonType": "array",
            #                         "description": "Articles for motosport",
            #                         "items": article_schema
            #                     },
            #                     "science": {
            #                         "bsonType": "array",
            #                         "description": "Articles for science",
            #                         "items": article_schema
            #                     },
            #                     "space": {
            #                         "bsonType": "array",
            #                         "description": "Articles for space",
            #                         "items": article_schema
            #                     },
            #                     "technology": {
            #                         "bsonType": "array",
            #                         "description": "Articles for technology",
            #                         "items": article_schema
            #                     },
            #                     "war": {
            #                         "bsonType": "array",
            #                         "description": "Articles for war",
            #                         "items": article_schema
            #                     },
            #                 }
            #             }
            #         }
            #     }
            # })
            self.education = self.db.create_collection("education", check_exists=True,
                                                       validator={"$jsonSchema": article_schema})
            self.health = self.db.create_collection("health", check_exists=True,
                                                    validator={"$jsonSchema": article_schema})
            self.business = self.db.create_collection("business", check_exists=True,
                                                      validator={"$jsonSchema": article_schema})
            self.motosport = self.db.create_collection("motorsport", check_exists=True,
                                                       validator={"$jsonSchema": article_schema})
            self.science = self.db.create_collection("science", check_exists=True,
                                                     validator={"$jsonSchema": article_schema})
            self.space = self.db.create_collection("space", check_exists=True,
                                                   validator={"$jsonSchema": article_schema})
            self.technology = self.db.create_collection("technology", check_exists=True,
                                                        validator={"$jsonSchema": article_schema})
            self.war = self.db.create_collection("war", check_exists=True, validator={"$jsonSchema": article_schema})

        except CollectionInvalid as ci:
            print(f"You probably do not have the right access or the collection already exists {ci}")
        finally:
            self.education = self.db["education"]
            self.health = self.db["health"]
            self.business = self.db["business"]
            self.motosport = self.db["motorsport"]
            self.science = self.db["science"]
            self.space = self.db["space"]
            self.technology = self.db["technology"]
            self.war = self.db["war"]

        try:
            self.users = self.db.create_collection("users", check_exists=True, validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["email"],
                    "properties": {
                        "keywords": {
                            "bsonType": "array",
                            "description": "Topics the user is interested in"
                        },
                        "created": {
                            "bsonType": "date",
                            "description": "The date which the user was created"
                        },
                        "email": {
                            "bsonType": "string",
                            "pattern": "[\w-\.]+@([\w-]+\.)+[\w-]{2,4}",
                            "description": "User's email required"
                        },
                        "city": {
                            "bsonType": "string",
                            "description": "The city the user lives!"
                        }
                    }
                }
            })
        except CollectionInvalid as ci:
            print(f"You probabli do not have the right access or the collection already exists {ci}")
        finally:
            self.users = self.db["users"]

    # User Functions
    def create_user(self, data):
        existing_document = self.users.find_one({"email": data["email"]})
        if not existing_document:
            data['created'] = datetime.now()

            inserted = self.users.insert_one(data)

            return "Inserted ID" + str(inserted.inserted_id)
        else:
            return "There is an existing user with this creds"

    def edit_user_keywords(self, email, data):
        myquery = {"email": email}
        newvalues = {"$set": data}

        existing_document = self.users.find_one({"email": email})
        if existing_document:
            try:
                self.users.update_one(myquery, newvalues)
                return "The user's keywords updated successfully!"
            except Exception as e:
                print(e)
                return "There was an error while updating the users values"
        else:
            return "There is no user with this email address"

    def delete_user(self, email):
        # TODO - normaly after some authentication
        existing_document = self.users.find_one({"email": email})
        if existing_document:
            try:
                self.users.delete_one({"email": email})
                return {
                    "status": 200,
                    "data": f"The user with email address {email} deleted successfully"
                }
            except Exception as e:
                print(e)
                return {
                    "status": 500,
                    "description": f"There was an error while trying to delete the user with email {email}"
                }
        else:
            return {
                "status": 400,
                "description": f"There there is no user with email {email}"
            }

    def find_articles(self, email):
        articles = {}
        sources_desc = {}

        user = self.users.find_one(filter={"email": email})
        if user:
            user_topics = user['keywords']
            for topic in user_topics:

                cursor_article = self.db[f"{topic}"].find().limit(10)
                articles[topic] = [] 
                sources = []
                for article in cursor_article:

                    art_cont = article["article"]
                    src = article["source"]
                    
                    articles[topic].append({
                        "article": art_cont,
                        "source": src
                    })
                    

                    if src not in sources:
                        sources.append(src)

                    for source in sources:
                        if self.sourceDomainName.find_one({"source": source}):
                            sources_desc[source] = self.sourceDomainName.find_one(
                                {"source": source}, {"_id": 0, "source": 1, "description": 1}
                            )

            return {
                "status": 200,
                "data": {
                    "user_articles": articles,
                    "Sources Descriptions": sources_desc
                }
            }

        return {
            "status": 400,
            "description": f"There there is no user with email {email}"
        }

    #### Topics Functions ####
    def insert_article(self, topic, articles):
        try:
            self.db[f'{topic}'].insert_many(articles)
            return {
                "status": 200,
                "data": "The articles added successfully"
            }
        except Exception as e:
            logging.exception(e)
        return {
            "status": 500,
            "description": "Something whent wrong while trying to update the topic's article list"
        }

    def insert_source_info(self, source_name, source_info):
        try:
            if not self.sourceDomainName.find_one({"source":source_name}):
                self.sourceDomainName.insert_one({"source":source_name,"description":source_info})
                return {
                "status": 200,
                "data": "The source was added!!!!!!"
                }
            else:
                return {
                "status": 500,
                "data": "The source is already inserted"
            }
            
        except Exception as e:
            logging.exception(e)
        return {
            "status": 500,
            "description": "Something whent wrong while trying to update the topic's article list"
        }



class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return str(o)

        if isinstance(o, ObjectId):
            return str(o)

        return json.JSONEncoder.default(self, o)
