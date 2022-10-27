from flask import Flask
from pymongo import MongoClient

#Name of the application module or package so flask knows where to look for resources
app = Flask(__name__)

#controllers implementations
@app.get("/user/articles/<int:user_id>")
def fetch_users_articles_controller():
    return "<p>Return users articles bases on id of fail if invalid user id is provided</p>"


@app.post("/create/user")
def create_user_controller():
    return "<p>here a new user should be added to the db with the keywords that he is interested in</p>"


@app.put("/edit/user/keywords/<int:user_id>")
def add_new_user_controller():
    return "<p>imp[lement a solution where we can edit the users keywords</p>"

@app.delete("/delete/user")
def delete_user_controller():
    return "<p>delete a user from the collection</p>"

def get_db():
    client = MongoClient(host='mongodb_container',
                         port=27017,
                         username='root',
                         password='rootpassword')

    db = client["articles_keywords_db"]

    #creating our collections( For some reason if we dont add an item it will not show when you call db.list_collection_names()
    #But at the same times its created and ready to use
    colection_f1 = db["motosport"]
    #.. Add all the topics we want to have
    collection_sd_name = db["source_domain_name"]
    collection_users = db["users"]

    return db

if __name__ == "__main__":
    #Creating a new connection with mongo
    db = get_db()

    app.run(port=8080, host="0.0.0.0")
