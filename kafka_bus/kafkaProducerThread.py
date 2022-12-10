from kafka import KafkaProducer
from threading import Thread
import time
from apis.newsapi import NewsApi
from apis.mediawiki import MediaWikiApi

class KafkaProducerThread(Thread):
    def __init__(self,TOPICS):
        Thread.__init__(self)
        self.topics = TOPICS
        self.news_api = NewsApi()
        self.media_api = MediaWikiApi()


    def run(self):
        # Initialize the Kafka producer
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
            max_block_ms=100000,)

        # Function to call the News API and publish the retrieved articles to the corresponding Kafka topic
        def call_apis():
            # Iterate over the keywords
            for topic in self.topics:
                articles = self.news_api.get_articles(topic)
                for article in articles:
                    if article:
                        producer.send(topic,article)
                        source_info = self.media_api.get_source_domain_info(article["source"])
                        if source_info:
                            # Publish source domain name information to "sources" topic
                            producer.send("sources", value=source_info)

            # Flush the producer to ensure all messages are sent
            producer.flush()

        # Call the News API every 2 hours
        while True:
            call_apis()
            time.sleep(7200)
            