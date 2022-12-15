import json
from kafka import KafkaConsumer
import logging


class KafkaConsumerThread:
    def __init__(self, topics, db):
        self.topics = topics
        self.db = db
        self.log = logging.getLogger("my-logger")

    def start(self):
        self.log.info("Start Consumer Thread")

        consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=True,
                                 value_deserializer=json.loads)
        for topic in self.topics:
            consumer.subscribe(topic)

            for message in consumer:
                self.log.info(message)
                self.db.insert_article(message.topic, [message.value])

        source_consumer = KafkaConsumer('sources', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest',
                                        value_deserializer=json.loads)

        for message in source_consumer:
            self.log.info(message)
            self.db.insert_source_info(message.value["source_name"], message.value["source_info"])



