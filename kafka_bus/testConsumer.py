from kafka import KafkaConsumer
from json import loads
from time import sleep


TOPICS= ["agricuture",
        "bussines",
        "elon-musk",
        "motosport",
        "science",
        "space",
        "technology",
        "war"]

consumer = KafkaConsumer(
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            value_deserializer=lambda x: loads(x),
            group_id="my-group",)

consumer.subscribe(TOPICS)
keywords = TOPICS

for message in consumer:
    
    collection = message.value
    print(collection)