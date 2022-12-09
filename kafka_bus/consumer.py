from kafka import KafkaConsumer
from json import loads
from time import sleep
import logging
from assets.keywords import Keywords


# Init
class Consumer():
    def __init__(self,TOPICS):
        self.consumer = KafkaConsumer(
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            value_deserializer=lambda x: loads(x),
            group_id="my-group",)

        self.consumer.subscribe(TOPICS)
        self.keywords = TOPICS
        self.file = open("text.txt","a")
        self.keywords = Keywords()

    def save_to_mongo(self):
        for message in self.consumer:
            collection = message.value
            logging.warning(collection)
            print(collection, flush=True)
            self.keywords.create(collection)
            # if message.topic in self.keywords:
            #     collection = message.value
            #     print(collection, flush=True)
            #     # collection = db[message.topic]
            #     # collection.insert_one(message.value)
            # elif message.topic == 'sources':
            #     sources= message.value
                # sources = db['sources']
                # sources.insert_one(message.value)