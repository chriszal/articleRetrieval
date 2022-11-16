
from flask import Flask, request, jsonify
from assets.users import User
from apis.newsapi import NewsApi

#Name of the application module or package so flask knows where to look for resources
app = Flask(__name__)

#controllers implementations
user = User()
news=NewsApi()

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
    response = user.create(data)

    return  response, 201


@app.put("/edit/user/keywords/<string:email>")
def add_new_user_controller(email):
    data = request.get_json()
    response = user.update(email, data)
    return response, 201

@app.delete("/delete/user/<string:email>")
def delete_user_controller(email):
    count = user.delete(email)
    return "Deleted entities: "+str(count)



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
    app.run(port=8080, host="0.0.0.0")
    


