import json
from kafka import KafkaConsumer
import logging
import time


class KafkaConsumerThread:
    def __init__(self, topics, db):
        self.topics = topics
        self.db = db
        self.log = logging.getLogger("my-logger")

    def start(self):
         # Wait for a few seconds before starting the Kafka consumer
        self.log.info("Start Consumer Thread")
        time.sleep(20)
        consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                                 auto_offset_reset='latest',
                                 enable_auto_commit=True,
                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        consumer.subscribe(self.topics)
        for message in consumer:
            self.log.info(message)
            self.db.insert_article(message.topic, [message.value])

        source_consumer = KafkaConsumer('sources', bootstrap_servers=['localhost:9092'], auto_offset_reset='latest',enable_auto_commit=True,
                                        value_deserializer=lambda x: json.loads(x.decode('utf-8')))

        for message in source_consumer:
            self.log.info(message)
            self.db.insert_source_info(message.value["source_name"], message.value["source_info"])



