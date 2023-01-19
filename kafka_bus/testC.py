from kafka import KafkaConsumer
from threading import Thread
import json
from concurrent.futures import ThreadPoolExecutor
# from assets.database import Database
import json
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId, json_util
from pymongo.errors import CollectionInvalid
import logging
from bson.json_util import dumps




class KafkaConsumerThread:
    def __init__(self, topics):
        self.topics = topics
        self.log = logging.getLogger("my-logger")

    def start(self):
        print("test")
        # Wait for a few seconds before starting the Kafka consumer
        # time.sleep(20)
        # self.log.info("Start Consumer Thread")

        consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=True,
                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        consumer.subscribe(self.topics + ["sources"])

        processed_keys = set()

        for message in consumer:
            if message.key in processed_keys:
                # skip this message, as it's a duplicate
                # print("duplicates")
                continue
            else:
                processed_keys.add(message.key)
                print(message.topic)
            # if message.topic == "sources":
            #     print(message.value["source_info"])
            #     # self.db.insert_source_info(message.value["source_name"], message.value["source_info"])
            # else:
            #     print(message.value)
                # self.db.insert_article(message.topic, [message.value])

        # source_consumer = KafkaConsumer('sources', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest',
        #                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')))

        # for message in source_consumer:
        #     print(message.message)
        # self.db.insert_source_info(message.value["source_name"], message.value["source_info"])


if __name__ == "__main__":
    TOPICS = ["government",
              "health",
              "business",
              "motorsport",
              "science",
              "space",
              "technology",
              "war"]
    executor = ThreadPoolExecutor(max_workers=1)

    # Create the Kafka producer thread
    thread = KafkaConsumerThread(TOPICS)

    # Start the Kafka producer thread
    future = executor.submit(thread.start)
