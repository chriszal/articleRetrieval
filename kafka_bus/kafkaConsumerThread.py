import logging
from kafka import KafkaConsumer
from threading import Thread
import json


class KafkaConsumerThread(Thread):
    def __init__(self, TOPICS,db):
        Thread.__init__(self)
        self.topics = TOPICS
        self.db= db

    def run(self):
        print("Start Consumer Thread")
        consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=True, value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        for topic in self.topics:
            consumer.subscribe(topic)

            # Iterate over the messages in the topic
            for message in consumer:
                logging.info(message)
                self.db.insert_article(message.topic,[message.value])
                    
                # Save articles in corresponding MongoDB collection
                # self.db.keywords.insert_one(message.value)

        # Initialize the Kafka consumer for the sources topic
        source_consumer = KafkaConsumer('sources', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest',
                                        value_deserializer=lambda x: json.loads(x.decode('utf-8')))

        for message in source_consumer:
            logging.info(message)
            self.db.insert_source_info(message.value["source_name"],message.value["source_info"])
            # Save source domain name information in "sources" collection
            # self.db.sourceDomainName.insert_one(message.value)
