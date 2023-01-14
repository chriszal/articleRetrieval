import json
from kafka.errors import NoBrokersAvailable
from kafka import KafkaConsumer
import logging
import time


class ConnectionException(Exception):
    pass


class KafkaConsumerThread:
    def __init__(self, topics, db):
        self.topics = topics
        self.db = db
        # self.logger = logging.getLogger()
        # self.logger.debug("Initializing the consumer")

    def start(self):
        # Wait for a few seconds before starting the Kafka consumer
        # time.sleep(15)
        # self.logger.debug("Getting the kafka consumer")
        try:
            consumer = KafkaConsumer(bootstrap_servers=['kafka:29092'],
                                     auto_offset_reset='earliest',
                                     enable_auto_commit=True,
                                     value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        except NoBrokersAvailable as err:
            # self.logger.error("Unable to find a broker: {0}".format(err))
            time.sleep(1)
        consumer.subscribe(self.topics + ["sources"])

        # try:
        # if consumer:
        for message in consumer:
            if message.topic == "sources":
                self.db.insert_source_info(message.value["source_name"], message.value["source_info"])
            else:
                self.db.insert_article(message.topic, [message.value])
            # raise ConnectionException
        # except AttributeError as ae:
        #     self.logger.error("Unable to retrieve the message.  "
        #                       "There is no consumer to read from.")
        #     self.logger.error(str(ae))
        #     raise ConnectionException
