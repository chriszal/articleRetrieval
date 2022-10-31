class User(db.Document):
    keywords = db.ListField()
    email = db.StringField(required=True,unique=True)
    city = db.StringField()
    timestamp = db.DoubleField()