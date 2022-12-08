from newsapi import NewsApiClient
import requests

# Init
class NewsApi():
    def __init__(self):
        self.secret = "2a2624e83ecb4b7f9a3e8bc1798d6946"

    def get_articles(self,keyword):
        response = requests.get("https://newsapi.org/v2/everything",params={'q':keyword,'apiKey': self.secret })
        articles=[]
        for article in response['articles']:
            source = article['source']['name']
            articles.append({'source':source,'article':article})
        
        return articles