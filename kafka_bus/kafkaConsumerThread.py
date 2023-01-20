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
        self.processed_keys = set()

    def start(self):
        print("in consumer")
        self.logger.debug("Getting the kafka consumer")
        try:
            consumer = KafkaConsumer(bootstrap_servers=['kafka:29092'],
                                     auto_offset_reset='earliest',
                                     enable_auto_commit=True,
                                    #  group_id='my_group',
                                     value_deserializer=lambda x: json.loads(x.decode('utf-8')))
            print("found broker")
            print("before subscription")
            consumer.subscribe(self.topics + ["sources"])

            for message in consumer:
                self.logger.info(message)
                if message.key in self.processed_keys:
                    # skip this message, as it's a duplicate
                    continue
                else:
                    self.processed_keys.add(message.key)
                    if message.topic == "sources":
                        self.db.insert_source_info(message.value["source_name"], message.value["source_info"])
                    else:
                        self.db.insert_article(message.topic, [message.value])
        except NoBrokersAvailable as err:
            print("No brokers")
            self.logger.error("Unable to find a broker: {0}".format(err))
        
        
            
