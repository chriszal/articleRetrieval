from threading import Timer
import json
from apis.newsapi import NewsApi
from apis.mediawiki import MediaWikiApi
from kafka import KafkaProducer
import time
import logging


def call_apis(self,topics, news_api, media_api):
    producer = KafkaProducer(bootstrap_servers=['kafka:29092'],
        max_block_ms=100000,
        value_serializer=lambda x: json.dumps(x).encode('utf-8'))

    domains = []

    for topic in topics:
        articles = news_api.get_articles(topic)
        for article in articles:
            if article['source'] != '':
                if article['source'] not in domains:
                    domains.append(article['source'])
                self.log.info(article['source'])

                producer.send(topic, value=article)
                producer.flush()
    for domain in domains:
        source_info = media_api.get_source_domain_info(domain)
        if source_info:
            
            producer.send("sources", value={"source_name": domain, "source_info": source_info})

            # Flush the producer to ensure all messages are sent
            producer.flush()

class KafkaProducerThread:
    def __init__(self, topics):
        self.topics = topics
        self.news_api = NewsApi()
        self.media_api = MediaWikiApi()
        self.log = logging.getLogger("my-logger")
        self.log.info(("init"))


    def start(self):
        self.log.info("starts")
        # Call the APIs immediately when the thread starts
        call_apis(self,self.topics, self.news_api, self.media_api)

        # Use a timer to schedule the next API call
        timer = Timer(7200, self.start)
        timer.start()



