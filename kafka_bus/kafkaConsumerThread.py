from kafka import KafkaConsumer
from threading import Thread
from flask import jsonify

class KafkaConsumerThread(Thread):
    def __init__(self, user_id):
        Thread.__init__(self)
        self.user_id = user_id
        self.TOPICS = ["agricuture",
            "health",
            "business",
            "motosport",
            "science",
            "space",
            "technology",
            "war"]

    def run(self):
        # Initialize an empty list to store the articles
        articles = []

        # Iterate over the keywords
        for keyword in self.TOPICS:
            # Initialize the Kafka consumer for the keyword's topic
            consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                auto_offset_reset='earliest',
                enable_auto_commit=True)
            consumer.subscribe(keyword)
            # Iterate over the messages in the topic
            for message in consumer:
                # Get the article
                article = message.value

                # Get the source domain name
                source_domain = article['source']

                # Search for information about the source on Wikipedia
                # search_wikipedia(source_domain)

                # # Check if the article is relevant to the user (i.e. matches the user's keywords and city)
                # if set(self.TOPICS).issubset(article['keywords']) and city == article['city']:
                #     # Add the article to the list
                #     articles.append(article)

        # Initialize the Kafka consumer for the sources topic
        consumer = KafkaConsumer('sources', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest')

        # Iterate over the messages in the topic
        for message in consumer:
            # Get the source description
            description = message.value

            # Find the article with the corresponding source domain name
            article = next((a for a in articles if a['source']['domain'] == description['domain']), None)

            # If the article was found, add the description to it
            if article is not None:
                article['source']['description'] = description

        # Return the articles to the user
        return jsonify(articles), 200
