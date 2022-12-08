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

        self.consumer.subscribe(TOPICS)

    def save_to_mongo(self,event):
        for event in self.consumer:
            event_data = event.value
            # Do whatever you want
            print(event_data)
            sleep(2)