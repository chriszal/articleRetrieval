import requests
from datetime import datetime
import time


# Init
class NewsApi():
    def __init__(self):
        # self.secret = "420d1582b00240789d9fc79e7943e61f"
        self.secret = "26201851ac9241ebab5eeb4bc239dfdd"

    def get_articles(self, keyword):
        response = requests.get("https://newsapi.org/v2/everything",
                                params={'q': keyword, 'apiKey': self.secret, 'language': 'en'})
        if response.status_code == 200:
            response_dict = response.json()
            articles = []

            for article in response_dict['articles']:
                source = article['source']['name']
                author = article['author']
                if author==None:
                    author = ""
                date_object = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
                unix_timestamp = int(time.mktime(date_object.timetuple()))
                articles.append({'source': source, 'article': article['content'], 'author': author,
                                 'timestamp': unix_timestamp})
            if not articles:
                articles = [{'source': '', 'article': '', 'author': '', 'timestamp': ''}]
            return articles
        else:
            return [{'source': '', 'article': '', 'author': '', 'timestamp': ''}]
