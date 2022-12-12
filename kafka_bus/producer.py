from json import dumps
from kafka import KafkaProducer
from apis.newsapi import NewsApi


class Producer():
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda x: dumps(x).encode('utf-8'))
        self.news_articles = NewsApi()

    def publish_articles_on_topic(self, topic):
        self.producer.send(topic, self.news_articles.get_articles(topic))
