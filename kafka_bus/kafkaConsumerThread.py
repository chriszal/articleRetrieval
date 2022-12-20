import json
from kafka import KafkaConsumer
import logging
import time


class KafkaConsumerThread:
    def __init__(self, topics, db):
        self.topics = topics
        self.db = db

    def start(self):
         # Wait for a few seconds before starting the Kafka consumer
        # time.sleep(15)
        consumer = KafkaConsumer(bootstrap_servers=['kafka:29092'],
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=True,
                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        consumer.subscribe(self.topics+["sources"])
        
        for message in consumer:
            if message.topic=="sources":
                self.db.insert_source_info(message.value["source_name"], message.value["source_info"])
            else:
                self.db.insert_article(message.topic, [message.value])


