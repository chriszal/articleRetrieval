from flask import Flask, jsonify, request
from assets.users import User
from kafka_bus.producer import Producer
from kafka_bus.consumer import Consumer
from kafka_bus.kafkaProducerThread import KafkaProducerThread
from kafka_bus.kafkaConsumerThread import KafkaConsumerThread
from assets.database import Database
import time
import threading
import logging
from assets.ArticleSDDescriptions import SourceDomainDescriptions
# import jellyfish

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
user = User()
db = Database()
sourceDomainDesc = SourceDomainDescriptions()

@app.route('/')
def index():
    return jsonify(
        status=True,
        message='Welcome !'
    )

# @app.get("/keyword/articles/<string:keyword>")
# def fetch_users_articles_controller(user_keyword):
#     """
#     :param keyword:
#     :return: The articles that corespond to this keyword

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

#     for keyword in keywords:

#         #Cosine similarity of the true title and the candidate
#         if jellyfish.jaro_distance(keyword, user_keyword) >= 0.85:
#             response = db.find_articles(user_keyword)
#             return response, 201

#     return "There are no anvailable records for the given keyword, please use one that is supported and try again", 500

# @app.get("/source/description/<string:sourcedomainname>")
# def fetch_users_articles_controller(sourcedomainname):
#     #TODO- actual api response
#     #Cosine similarity of the true title and the candidate
#     response = sourceDomainDesc.fetch_domain_descriptionzç(sourcedomainname)
#     return response


# @app.get("/user/articles/<int:user_id>")
# def fetch_users_articles_controller():
#     return "<p>Return users articles bases on id of fail if invalid user id is provided</p>"

@app.get('/articles/<email>')
def get_articles(email):
    # Start the consumer thread for the user
    consumer_thread = KafkaConsumerThread(email)
    consumer_thread.start()

    # Wait for the consumer thread to finish
    consumer_thread.join()

    # Return the articles to the user
    return consumer_thread.result

@app.post("/create/user")
def create_user_controller():
    data = request.get_json()
    response = user.create(data)

    return response, 201

@app.put("/edit/user/keywords/<string:email>")
def add_new_user_controller(email):
    data = request.get_json()
    response = user.update(email, data)
    return response, 201

@app.delete("/delete/user/<string:email>")
def delete_user_controller(email):
    count = user.delete(email)
    return "Deleted entities: " + str(count)

def run_producer():
    producer = Producer()
    while True:
        for topic in TOPICS:
            logging.warning(topic)
            producer.publish_articles_on_topic(topic)
        time.sleep(10)

def run_consumer():
    consumer = Consumer(TOPICS)
    consumer.save_to_mongo()

if __name__ == "__main__":
    # Creating a new connection with mongo
    app.run(port=8080, host="0.0.0.0")
    
    producer_thread = KafkaProducerThread()
    producer_thread.start()
    # threading.Thread(target=run_producer).start()
    # threading.Thread(target=run_consumer).start()
    
