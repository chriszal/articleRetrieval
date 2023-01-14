from flask import Flask, jsonify, request
from kafka_bus.kafkaProducerThread import KafkaProducerThread
from kafka_bus.kafkaConsumerThread import KafkaConsumerThread
from concurrent.futures import ThreadPoolExecutor
from assets.database import Database
from apis.mediawiki import MediaWikiApi
from apis.newsapi import NewsApi
import time
# import jellyfish
import logging
import threading

# Name of the application module or package so flask knows where to look for resources
app = Flask(__name__)

news_api = NewsApi()
media_api = MediaWikiApi()

TOPICS = Database.TOPICS
# controllers implementations

db = Database()


@app.route('/')
def index():
    # user = {
    #     "keywords": {"test": "test2"},
    #     "email": "test@gmail.com",
    #     "created": datetime.datetime.now(),
    #     "city": "Testssssasdbasud"
    # }
    #
    # insert_result = db.users.insert_one(user)
    #
    # print(insert_result)

    return jsonify(
        status=True,
        message='Welcome !'
    )


'''
 USER'S API METHODS
'''


@app.post("/user/create")
def create_user_controller():
    data = request.get_json()

    response = db.create_user(data)

    return {
        "satus": 201,
        "data": response,
    }


@app.put("/user/edit/keywords")
def edit_user_keywords_controller():
    email = request.args.get('email')
    data = request.get_json()

    response = db.edit_user_keywords(email, data)

    return {
        "satus": 200,
        "data": response,
    }


@app.get('/user/articles')
def get_articles():
    email = request.args.get("email")

    response = db.find_articles(email)

    # Return the articles to the user
    return response


@app.delete("/user/delete")
def delete_user_controller():
    email = request.args.get("email")

    response = db.delete_user(email)

    return response


'''
 Topics Controllers
'''


@app.put("/topics/add/article")
def add_articles_to_topic():
    topic = request.args.get("topic")
    data = request.get_json()

    response = db.insert_article(topic, data)

    return response


@app.get('/user/recommend')
def fetch_recommendation():
    email = request.args.get("email")
    article_id = request.args.get("id")

    return jsonify(
        status=True,
        message='Test recommendations'
    )


# @app.get("/topics/articles/<string:keyword>")
# def fetch_users_articles_controller(user_keyword):
#     """
#     :param keyword:
#     :return: The articles that correspond to the specified topic/keyword

#     """
#     for topic in TOPICS:
#         #Cosine similarity of the true title and the candidate
#         if jellyfish.jaro_distance(topic, user_keyword) >= 0.85:
#             response = db.find_articles(user_keyword)
#             return {
#                 "satus": 201,
#                 "data": response,
#             }

#     return "There are no anvailable records for the given keyword, please use one that is supported and try again", 500


'''
 Source Domain Controllers
'''


@app.get('/fetch')
def fetch_source():
    domains = []
    object = []
    for topic in TOPICS:
        articles = news_api.get_articles(topic)
        for article in articles:
            if article['source'] != '':
                if article['source'] not in domains:
                    domains.append(article['source'])
                # producer.send(topic,article)

    for domain in domains:
        source_info = media_api.get_source_domain_info(domain)
        if source_info:
            # producer.send("sources", value=source_info)
            object.append(source_info)
        else:
            object.append('')

    return jsonify(domains)


if __name__ == "__main__":
    # Creating a new connection with mongo
    # threading.Thread(target=lambda: app.run(port=8080, host="0.0.0.0",debug=True,use_reloader=False)).start()    

    executor = ThreadPoolExecutor(max_workers=3)
    producerThread = KafkaProducerThread(TOPICS)
    flaskThread = threading.Thread(target=lambda: app.run(port=8080, host="0.0.0.0", debug=True, use_reloader=False))
    executor.submit(flaskThread.start())
    time.sleep(15)
    executor.submit(producerThread.start)
    consumerThread = KafkaConsumerThread(TOPICS, db)
    executor.submit(consumerThread.start)
