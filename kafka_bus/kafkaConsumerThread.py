from kafka import KafkaConsumer
from threading import Thread
from flask import jsonify
from assets.database import Database

class KafkaConsumerThread(Thread):
    def __init__(self,TOPICS):
        Thread.__init__(self)
        self.topics = TOPICS
        self.db = Database()

    def run(self):
        print("Start Consumer Thread")
        self.db.keywords.insert_one({"t":"e"})
        for topic in self.topics:

            consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                auto_offset_reset='earliest',
                enable_auto_commit=True)

            consumer.subscribe(topic)

            # Iterate over the messages in the topic
            for message in consumer:
                print(message)
               # Save articles in corresponding MongoDB collection
                self.db.keywords.insert_one(message.value)

        # Initialize the Kafka consumer for the sources topic
        consumer = KafkaConsumer('sources', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest')

        for message in consumer:
            print(message)
            # Save source domain name information in "sources" collection
            self.db.ArticlesSDDescription.insert_one(message.value)

