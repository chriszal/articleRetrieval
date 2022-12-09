from kafka import KafkaProducer
from threading import Thread
import time
from apis.newsapi import NewsApi

class KafkaProducerThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.TOPICS = ["agricuture",
            "health",
            "business",
            "motosport",
            "science",
            "space",
            "technology",
            "war"]
        self.news_articles = NewsApi()


    def run(self):
        # Initialize the Kafka producer
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
            max_block_ms=100000,)

        # Function to call the News API and publish the retrieved articles to the corresponding Kafka topic
        def call_news_api():
            # Iterate over the keywords
            for topic in self.TOPICS:
                producer.send(topic,self.news_articles.get_articles(topic))

            # Flush the producer to ensure all messages are sent
            producer.flush()

        # Function to search for information about a source domain name on Wikipedia and publish it to the sources topic
        # def search_wikipedia(domain):
        #     # Search for the domain name on Wikipedia
        #     results = wiki.search(domain)

        #     # If there is a corresponding Wikipedia article, get its description and publish it to the sources topic
        #     if len(results) > 0:
        #         description = wiki.summary(results[0])
        #         producer.send('sources', value=description)

        #     # Flush the producer to ensure all messages are sent
        #     producer.flush()

        # Call the News API initially
        call_news_api()

        # Call the News API every 2 hours
        while True:
            time.sleep(7200)
            call_news_api()