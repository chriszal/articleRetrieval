from kafka import KafkaConsumer
from threading import Thread
from flask import jsonify

class KafkaConsumerThread(Thread):
    def __init__(self,TOPICS):
        Thread.__init__(self)
        self.topics = TOPICS

    def run(self):
        
        for topic in self.topics:

            consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                auto_offset_reset='earliest',
                enable_auto_commit=True)

            consumer.subscribe(topic)

            # Iterate over the messages in the topic
            for message in consumer:
               # Save articles in corresponding MongoDB collection
                mongo[topic].insert_one(message.value)

        # Initialize the Kafka consumer for the sources topic
        consumer = KafkaConsumer('sources', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest')

        for message in consumer:
            # Save source domain name information in "sources" collection
            mongo["sources"].insert_one(message.value)

