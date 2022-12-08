from kafka import KafkaConsumer
from json import loads
from time import sleep

# Init
class Consumer():
    def __init__(self,TOPICS):
        self.consumer = KafkaConsumer(
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            value_deserializer=lambda x: loads(x),
            group_id="my-group",)

        self.consumer.subscribe(TOPICS+["sources"])
        self.keywords = TOPICS

    def save_to_mongo(self):
        for message in self.consumer:
            if message.topic in self.keywords:
                collection = message.value
                # collection = db[message.topic]
                # collection.insert_one(message.value)
            elif message.topic == 'sources':
                sources= message.value
                # sources = db['sources']
                # sources.insert_one(message.value)