from kafka import KafkaConsumer
from threading import Thread
import json
# from assets.database import Database

class KafkaConsumerThread(Thread):
    def __init__(self,TOPICS):
        Thread.__init__(self)
        self.topics = TOPICS
        # self.db = Database()

    def run(self):
        print("Start Consumer Thread")
        consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,value_deserializer=lambda x: json.loads(x.decode('utf-8')))

        for topic in self.topics:

           
            consumer.subscribe(topic)

            # Iterate over the messages in the topic
            for message in consumer:
                if message.topic ==topic:
                    print(message.value)
               # Save articles in corresponding MongoDB collection
                # self.db.keywords.insert_one(message.value)

        # Initialize the Kafka consumer for the sources topic
        source_consumer = KafkaConsumer('sources', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest',value_deserializer=lambda x: json.loads(x.decode('utf-8')))

        for message in source_consumer:
            if message.topic =="sources":
                print(message.value)
            # Save source domain name information in "sources" collection
            # self.db.ArticlesSDDescription.insert_one(message.value)

if __name__ == "__main__":
    TOPICS= ["education",
            "health",
            "business",
            "motorsport",
            "science",
            "space",
            "technology",
            "war"]
    consumer_thread = KafkaConsumerThread(TOPICS)
    consumer_thread.start()