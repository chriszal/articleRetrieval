from json import dumps
from kafka import KafkaProducer
import time
import requests

TOPICS= ["agricuture",
        "bussines",
        "elon-musk",
        "motosport",
        "science",
        "space",
        "technology",
        "war"]

def get_articles(keyword):
        response = requests.get("https://newsapi.org/v2/everything",params={'q':keyword,'apiKey': "420d1582b00240789d9fc79e7943e61f"  ,'language':'en'})
        if response.status_code == 200:
            response_dict = response.json()
            articles=[]
        
            for article in response_dict['articles']:
                source = article['source']['name']
                articles.append({'source':source,'article':article['content']})
        
            if not articles:
                articles = [{'source': '', 'article': ''}]
            return articles
        else:
            return [{'source': '', 'article': ''}]

producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda x: dumps(x).encode('utf-8'),
            max_block_ms=100000,)


while True:
    for topic in TOPICS:
        print(topic)
        articles = get_articles(topic)
        producer.send(topic, articles)
    time.sleep(10)

