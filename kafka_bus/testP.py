from kafka import KafkaProducer
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from threading import Timer
from json import dumps
from datetime import datetime
from kafka.errors import KafkaError
import time
import json
# from apis.newsapi import NewsApi
# from apis.mediawiki import MediaWikiApi
from mediawiki import MediaWiki, DisambiguationError, PageError
from kafka.errors import NoBrokersAvailable
import hashlib
# Init
class MediaWikiApi():
    def __init__(self):
        self.mediawiki = MediaWiki()

    def get_source_domain_info(self, source_name):
        # Search for articles with the source domain name
        try:
            articles = self.mediawiki.page(source_name + " News")
            # print("test"+str(articles))
        except DisambiguationError as e:
            # Handle the case where multiple pages are found
            # return e.options
            # print(f"An error occurred: {e}")
            return self.mediawiki.page(e.options[0]).summary
        except PageError as e:
            # return e.message
            print(f"An error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        else:
            # Return the first article's description
            return articles.summary


import requests


# Init
class NewsApi():
    def __init__(self):
        self.secret = "2a2624e83ecb4b7f9a3e8bc1798d6946"

    def get_articles(self, keyword):
        response = requests.get("https://newsapi.org/v2/everything",
                                params={'q': keyword, 'apiKey': self.secret, 'language': 'en'})
        if response.status_code == 200:
            response_dict = response.json()
            # print(response_dict)
            articles = []

            for article in response_dict['articles']:
                source = article['source']['name']
                author = article['author']
                if author==None:
                    author = ''
                date_object = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
                unix_timestamp = int(time.mktime(date_object.timetuple()))
                articles.append({'source': source, 'article': article['content'], 'author': author,
                                 'timestamp': unix_timestamp})
            if not articles:
                articles = [{'source': '', 'article': '', 'author': '', 'timestamp': ''}]
            return articles
        else:
            return [{'source': '', 'article': '', 'author': '', 'timestamp': ''}]

    #     articles =[]
    # for keyword in keywords:
    #     articles.append(news.get_articles(keyword))
    #     # sources.get_source_domain_info(articles['source'])
    # # s = wiki.get_source_domain_info(articles['source'])

    # # if articles:
    # return articles ,201


def call_apis(topics, news_api, media_api):
    
    try:

        producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             max_block_ms=100000,
                             value_serializer=lambda x: dumps(x).encode('utf-8'))
        print("In")
    except NoBrokersAvailable as err:
        print(err)
    domains = []

    for topic in topics:
        print(topic)
        articles = news_api.get_articles(topic)
        # print(articles)
        for article in articles:
            # print(article)
            if article['source'] != '':
                if article['source'] not in domains:
                    domains.append(article['source'])
                # print(article)
                key = article['author'] +"_"+str(article['timestamp'])
                # print(key.encode())
                future = producer.send(topic, key=key.encode(), value=article)
                try:
                    record_metadata = future.get(timeout=10)
                    producer.flush()
                    print(record_metadata)
                except KafkaError as e:
                    # Decide what to do if produce request failed...
                    print(e)
    for domain in domains:
        source_info = media_api.get_source_domain_info(domain)
        if source_info:
            print(domain)
            try:
                producer.send("sources",key=domain.encode(), value={"source_name": domain, "source_info": source_info})

                # Flush the producer to ensure all messages are sent
                producer.flush()
            except Exception as e:
                print("e2")

    # Flush the producer to ensure all messages are sent
    producer.close()

class KafkaProducerThread:
    def __init__(self, topics):
        self.topics = topics
        self.news_api = NewsApi()
        self.media_api = MediaWikiApi()

    def start(self):
        print("Start")
        # Wait for a few seconds before starting the Kafka consumer
        # Call the APIs immediately when the thread starts
        
        while True:
            call_apis(self.topics, self.news_api, self.media_api)
            time.sleep(10)
        # Use a timer to schedule the next API call
        # timer = Timer(10, self.start)
        # timer.start()


if __name__ == "__main__":
    TOPICS = ["education",
              "health",
              "business",
              "motorsport",
              "science",
              "space",
              "technology",
              "war"]
    # Initialize the thread pool with a single thread
    executor = ThreadPoolExecutor(max_workers=1)

    # Create the Kafka producer thread
    thread = KafkaProducerThread(TOPICS)

    # Start the Kafka producer thread
    future = executor.submit(thread.start)

    # try:
    #     future.get(TimeoutError=10)
# future = producer.send(topic, key=key, value=article)
#                 producer.flush()

#                 try:
#                     record_metadata = future.get(timeout=10)
#                     print(record_metadata)
#                 except KafkaError as e:
#                     # Decide what to do if produce request failed...
#                     print(e)