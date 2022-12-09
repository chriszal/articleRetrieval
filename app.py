from flask import Flask, jsonify, request
from kafka_bus.kafkaProducerThread import KafkaProducerThread
from kafka_bus.kafkaConsumerThread import KafkaConsumerThread
from assets.database import Database
import time
import logging
# import jellyfish
import datetime
from assets.models import Users

# Name of the application module or package so flask knows where to look for resources
app = Flask(__name__)

TOPICS= ["agricuture",
        "health",
        "business",
        "motosport",
        "science",
        "space",
        "technology",
        "war"]
# controllers implementations

db = Database()


@app.route('/')
def index():
    user = {
        "keywords": ["test", "test2"],
        "email": "test@gmail.com",
        "created": datetime.datetime,
        "city": "Testssssasdbasud"
    }

    user = Users(**user)

    insert_result = db.users.insert_one(user.to_bson())

    print(insert_result)
    print(user.to_bson())

    return jsonify(
        status=True,
        message='Welcome !'
    )


# @app.get("/keyword/articles/<string:keyword>")
# def fetch_users_articles_controller(user_keyword):
#     """
#     :param keyword:
#     :return: The articles that corespond to this keyword
#
#     :Note: The available keywords the user can enter here are
#       [
#         agricuture,
#         bussines,
#         elon musk,
#         motosport,
#         science,
#         space,
#         tech,
#         war
#     """
#     keywords = [
#         "agricuture",
#         "bussines",
#         "elon musk",
#         "motosport",
#         "science",
#         "space",
#         "technology",
#         "war"
#     ]
#
#     for keyword in keywords:
#
#         #Cosine similarity of the true title and the candidate
#         if jellyfish.jaro_distance(keyword, user_keyword) >= 0.85:
#             response = db.find_articles(user_keyword)
#             return response, 201
#
#     return "There are no anvailable records for the given keyword, please use one that is supported and try again", 500

# @app.get("/source/description/<string:sourcedomainname>")
# def fetch_users_articles_controller(sourcedomainname):
#     #TODO- actual api response
#     #Cosine similarity of the true title and the candidate
#     response = sourceDomainDesc.fetch_domain_descriptionzç(sourcedomainname)
#     return response
#
#
# @app.get("/user/articles/<int:user_id>")
# def fetch_users_articles_controller():
#     return "<p>Return users articles bases on id of fail if invalid user id is provided</p>"

# @app.get('/articles/<email>')
# def get_articles(email):
#     # Start the consumer thread for the user
#     consumer_thread = KafkaConsumerThread(email)
#     consumer_thread.start()

#     # Wait for the consumer thread to finish
#     consumer_thread.join()

#     # Return the articles to the user
#     return consumer_thread.result

# @app.post("/create/user")
# def create_user_controller():
#     data = request.get_json()
#     response = user.create(data)

#     return response, 201

# @app.put("/edit/user/keywords/<string:email>")
# def add_new_user_controller(email):
#     data = request.get_json()
#     response = user.update(email, data)
#     return response, 201

# @app.delete("/delete/user/<string:email>")
# def delete_user_controller(email):
#     count = user.delete(email)
#     return "Deleted entities: " + str(count)

#
# @app.post("/create/user")
# def create_user_controller():
#     data = request.get_json()
#     response = user.create(data)
#
#     return response, 201
#
# @app.put("/edit/user/keywords/<string:email>")
# def add_new_user_controller(email):
#     data = request.get_json()
#     response = user.update(email, data)
#     return response, 201
#
# @app.delete("/delete/user/<string:email>")
# def delete_user_controller(email):
#     count = user.delete(email)
#     return "Deleted entities: " + str(count)


@app.get('/users/<string:email>')
def get_user_articles(email):
    # get the user's preferences
    user = db.users.find_one({'_id': email})

    # create a dictionary to hold the articles grouped by source
    sources = {}

    # get the articles for each keyword the user is interested in
    for keyword in user['keywords']:

        # get the articles from the corresponding topic collection
        articles = list(db.keywords.find())

        # group the articles by source
        for article in articles:
            source = article['source']
            if source not in sources:
                sources[source] = []
            sources[source].append(article)

    # for each source, get its description from the sources collection if available
    for source, articles in sources.items():
        description = sources.find_one({'_id': source})
        if description:
            sources[source]['description'] = description['description']

    # return the articles grouped by source
    return jsonify(sources)

if __name__ == "__main__":
    # Creating a new connection with mongo
    app.run(port=8080, host="0.0.0.0")
    
    producer_thread = KafkaProducerThread(TOPICS)
    producer_thread.start()
    consumer_thread = KafkaConsumerThread(TOPICS)
    consumer_thread.start()
    # threading.Thread(target=run_producer).start()
    # threading.Thread(target=run_consumer).start()
    
