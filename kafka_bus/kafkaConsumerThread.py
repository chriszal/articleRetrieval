import json
from kafka.errors import NoBrokersAvailable
from kafka import KafkaConsumer
import logging
import time


class ConnectionException(Exception):
    pass


class KafkaConsumerThread:
    def __init__(self, topics, db,logger):
        self.topics = topics
        self.db = db
        self.logger = logger

    def start(self):
        self.logger.debug("Getting the kafka consumer")
        try:
            consumer = KafkaConsumer(bootstrap_servers=['kafka:29092'],
                                     auto_offset_reset='earliest',
                                     enable_auto_commit=True,
                                     value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        except NoBrokersAvailable as err:
            self.logger.error("Unable to find a broker: {0}".format(err))
            time.sleep(1)
        consumer.subscribe(self.topics + ["sources"])

        for message in consumer:
            self.logger(message)
            if message.topic == "sources":
                self.db.insert_source_info(message.value["source_name"], message.value["source_info"])
            else:
                self.db.insert_article(message.topic, [message.value])
        
