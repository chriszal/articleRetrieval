from time import sleep
from json import dumps
from kafka import KafkaProducer


class Producer():
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda x: dumps(x).encode('utf-8'))


    def publish_articles(self,articles):
        for article in articles:
            source = article['source']
            article = article['article']
            self.producer.send(source,article)

