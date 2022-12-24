from kafka import KafkaProducer
from threading import Thread
import time
import json
# from apis.newsapi import NewsApi
# from apis.mediawiki import MediaWikiApi
from mediawiki import MediaWiki, DisambiguationError, PageError

# Init
class MediaWikiApi():
    def __init__(self):
        self.mediawiki = MediaWiki()

    def get_source_domain_info(self, source_name):
        # Search for articles with the source domain name
        try:
            articles = self.mediawiki.page(source_name)
        except DisambiguationError as e:
            # Handle the case where multiple pages are found
            return e.options
        except PageError as e:
            return e.message
        else:
            # Return the first article's description
            return articles.summary

import requests

# Init
class NewsApi():
    def __init__(self):
        self.secret = "2a2624e83ecb4b7f9a3e8bc1798d6946"

    def get_articles(self,keyword):
        response = requests.get("https://newsapi.org/v2/everything",params={'q':keyword,'apiKey': self.secret ,'language':'en'})
        if response.status_code == 200:
            response_dict = response.json()
            articles=[]
        
            for article in response_dict['articles']:
                source = article['source']['name']
                articles.append({'source':source,'article':article['content']})
        
            if not articles:
                articles = [{'source': '', 'article': ''}]
            return articles
        else:
            return [{'source': '', 'article': ''}]
        
    #     articles =[]
    # for keyword in keywords:
    #     articles.append(news.get_articles(keyword))
    #     # sources.get_source_domain_info(articles['source'])
    # # s = wiki.get_source_domain_info(articles['source'])

    # # if articles:
    # return articles ,201

class KafkaProducerThread(Thread):
    def __init__(self,TOPICS):
        Thread.__init__(self)
        self.topics = TOPICS
        self.news_api = NewsApi()
        self.media_api = MediaWikiApi()


    def run(self):
        # Initialize the Kafka producer
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
            max_block_ms=100000,
            value_serializer=lambda x: json.dumps(x).encode('utf-8'))

        # Function to call the News API and publish the retrieved articles to the corresponding Kafka topic
        def call_apis():
            # Iterate over the keywords
            domains=[]
            for topic in self.topics:
                articles = self.news_api.get_articles(topic)
                for article in articles:
                    if article['source'] != '':
                        if article['source'] not in domains:
                            domains.append(article['source'])
                        producer.send(topic,value=article)
            
            for domain in domains:
                source_info = self.media_api.get_source_domain_info(domain)
                if source_info:
                    producer.send("sources", value=source_info)
                    
            # Flush the producer to ensure all messages are sent
            # producer.flush()

        # Call the News API every 2 hours
        while True:
            call_apis()
            time.sleep(50)
            
if __name__ == "__main__":
    TOPICS= ["education",
            "health",
            "business",
            "motorsport",
            "science",
            "space",
            "technology",
            "war"]
    consumer_thread = KafkaProducerThread(TOPICS)
    consumer_thread.start()