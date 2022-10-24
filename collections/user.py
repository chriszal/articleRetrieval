from mongoengine import *

class User(Document):
    keywords = ListField()
    email = StringField(required=True,unique=True)
    city = StringField()
    timestamp = DoubleField()