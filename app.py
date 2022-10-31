from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
import time as ts

#Name of the application module or package so flask knows where to look for resources
app = Flask(__name__)

#controllers implementations

@app.route('/')
def index():
    return jsonify(
        status=True,
        message='Welcome !'
    )

@app.get("/user/articles/<int:user_id>")
def fetch_users_articles_controller():
    return "<p>Return users articles bases on id of fail if invalid user id is provided</p>"


@app.post("/create/user")
def create_user_controller():
    data = request.get_json()
    data["timestamp"]=ts.time()
    

    db.user.insert_one(data)

    return jsonify(
        status=True,
        message='User saved successfully!'+str(data)
    ), 201


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

#TODO-close the db connection ( hint use decorators on events)
# @app.on_event("startup")
# def startup_db_client():
#     app.mongodb_client = MongoClient(host='mongodb_container',
#                          port=27017,
#                          username='root',
#                          password='rootpassword')
#     app.database = app.mongodb_client["articles_keywords_db"]
#     print("Connected to the MongoDB database!")
# @app.on_event("shutdown")
# def shutdown_db_client():
#     app.mongodb_client.close()


if __name__ == "__main__":
    #Creating a new connection with mongo
    db = get_db()
    app.run(port=8080, host="0.0.0.0")

