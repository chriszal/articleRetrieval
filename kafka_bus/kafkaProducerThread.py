from threading import Timer
import json
from apis.newsapi import NewsApi
from apis.mediawiki import MediaWikiApi
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from kafka.errors import KafkaError
import hashlib
import time
import logging


def call_apis(self, topics, news_api, media_api):
    print("in producer")
    try:
        producer = KafkaProducer(bootstrap_servers=['kafka:29092'],
                                 max_block_ms=100000,
                                #  group_id='my_group',
                                 value_serializer=lambda x: json.dumps(x).encode('utf-8'))
        # producer.create_topics(topics)
    except NoBrokersAvailable as err:
        self.logger.error("Unable to find a broker: {0}".format(err))
        time.sleep(1)

    domains = []
    try:
        if producer:
            for topic in topics:
                articles = news_api.get_articles(topic)
                for article in articles:
                    if article['source'] != '':
                        if article['source'] not in domains:
                            domains.append(article['source'])
                        key = article['author'] +"_"+str(article['timestamp'])
                    
                        future = producer.send(topic, key=key.encode(), value=article)
                        try:
                            record_metadata = future.get(timeout=10)
                            producer.flush()
                            # print(record_metadata)
                        except KafkaError as e:
                            # Decide what to do if produce request failed...
                            print(e)
                        
            for domain in domains:

                source_info = None

                if media_api != None:
                    source_info = media_api.get_source_domain_info(domain)

                if source_info:
                    future_s = producer.send("sources",key=domain.encode(), value={"source_name": domain, "source_info": source_info})

                    try:
                        record_metadata_s = future_s.get(timeout=10)
                        producer.flush()
                        logging.info(record_metadata_s)
                    except KafkaError as e:
                        # Decide what to do if produce request failed...
                        print(e)
            producer.close()
    except AttributeError:
        self.logger.error("Unable to send message. The producer does not exist.")



class KafkaProducerThread:
    def __init__(self, topics,logger):
        self.topics = topics
        self.news_api = NewsApi()
        self.media_api = None
        try:
            self.media_api = MediaWikiApi()
        except Exception as e:
            print(f"There was an exception raised! -> {e}. The app will try to re-start this process automatically")
        finally:
            try:
                for _ in range(2):
                    self.media_api = MediaWikiApi()
            except Exception as e:
                print(f"The program could not automatically restart the process -> {e}")
        self.logger = logger

    def start(self):
        # Call the APIs immediately when the thread starts
        call_apis(self, self.topics, self.news_api, self.media_api)

        # Use a timer to schedule the next API call in seconds
        timer = Timer(7200, self.start)
        timer.start()
