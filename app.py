from flask import Flask, jsonify, request, send_file
from kafka_bus.kafkaProducerThread import KafkaProducerThread
from kafka_bus.kafkaConsumerThread import KafkaConsumerThread
from concurrent.futures import ThreadPoolExecutor
from assets.database import Database
from apis.mediawiki import MediaWikiApi
from apis.newsapi import NewsApi
from graph.graphMigration import GraphMigration
import time
import threading
import networkx as nx
import logging

logging.basicConfig(level=logging.INFO)
# Name of the application module or package so flask knows where to look for resources
app = Flask(__name__)

"""
   Trying to automatically handle some basic and easy scenarios, so the app will not fall apart with the slightest interruption.
"""
try:
    news_api = NewsApi()
except Exception as e:
    print(f"There was an exception raised! -> {e}. The app will try to re-start this process automatically")
finally:
    try:
        for _ in range(2):
            news_api = NewsApi()
    except Exception as e:
        print(f"The program could not automatically restart the process -> {e}")

TOPICS = Database.TOPICS
# controllers implementations

# Initializing the database connection
db = Database()

# Creating the graph and edges from the articles in the database.
full_graph = GraphMigration(db, TOPICS)

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
 Article prediction endpoints
'''


@app.get('/user/articles/all')
def fetch_all_articles_with_id():
    response = db.fetch_all_articles()

    return response


@app.get('/user/articles/recommend')
def fetch_recommendation():
    article_id = request.args.get("id")

    #Updating the graph in order to have the updated graph unvailable for the user
    full_graph.update_graph()

    # Geting the actual graph, ready and connected!
    G = full_graph.get_graph()

    # TODO -Async call
    # #creating a thread excecutor instance in order to leverage async functions
    # executor = ThreadPoolExecutor(max_workers=3)

    """
        Here we are implementing a simple logic in order to recommend an article to the user
    """
    # here we find the neighbor node id's for the node(article) the user requested
    user_node_neighbors = [n for n in nx.all_neighbors(G, article_id)]

    # #Ading the requested node id along with the other in  order to take the right subgraph
    # user_node_neighbors.append(article_id)
    # #Here we are using the build in methods in order to get a sub-graph and apply a data mining algorithm
    # H = G.subgraph(user_node_neighbors)

    # Now we find the clossest node to the one requested, and return it to the user along with his original response
    cen_dict = nx.closeness_centrality(G)

    sorted_dict = {}
    sorted_keys = sorted(cen_dict, key=cen_dict.get, reverse=True)

    for w in sorted_keys:
        sorted_dict[w] = cen_dict[w]

    for node in sorted_dict:
        if node == article_id:
            max_deg = max(G.degree(user_node_neighbors))
            return {
                "status": 200,
                "Recommendation Article": G.nodes[max_deg[0]],
                "User Article": G.nodes[article_id]
            }

    #Here we are recomending something because we did not had any lack with the other mechanism.
    #This is an extreme corner case. And we try to recomend something instead of nothing.
    return {
        "status": 200,
        "Recommendation Article": G.nodes[list(sorted_dict.items())[0][0]],
        "User Article": G.nodes[article_id]
    }

    # communities_generator = nx.algorithms.community.girvan_newman(G)
    # top_level_communities = next(communities_generator)
    # next_level_communities = next(communities_generator)
    #
    # for community in next(communities_generator):
    #     for nodes in community:
    #         if article_id in nodes:
    #             return str(f"{[x for x in community], article_id}")
    # return str(type(communities_generator))
    #
    # return {
    #     "User Article": user_article
    #     "data": str(f"{[x for x in next_level_communities]}")
    # }
    # test node id -> "63c5b4aafd77d015069e499f"

"""
    Helper Functions
"""

if __name__ == "__main__":
    # Creating a new connection with mongo
    # threading.Thread(target=lambda: app.run(port=8080, host="0.0.0.0",debug=True,use_reloader=False)).start()
    executor = ThreadPoolExecutor(max_workers=3)
    producerThread = KafkaProducerThread(TOPICS,logging)
    consumerThread = KafkaConsumerThread(TOPICS, db, logging)

    flaskThread = threading.Thread(target=lambda: app.run(port=8080, host="0.0.0.0", debug=True, use_reloader=False))
    executor.submit(flaskThread.start())
    time.sleep(15)

    producerThread.start()
    consumerThread.start()
    
    
   
   
