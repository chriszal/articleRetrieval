import requests

# Init
class NewsApi():
    def __init__(self):
        self.secret = "2a2624e83ecb4b7f9a3e8bc1798d6946"

    def get_articles(self,keyword):
        response = requests.get("https://newsapi.org/v2/everything",params={'q':keyword,'apiKey': self.secret })
        if response.status_code == 200:
            response_dict = response.json()
            articles=[]
        
            for article in response_dict['articles']:
                source = article['source']['name']
                articles.append({'source':source,'article':article['content']})
        
            return articles
        else:
            return None
        
    #     articles =[]
    # for keyword in keywords:
    #     articles.append(news.get_articles(keyword))
    #     # sources.get_source_domain_info(articles['source'])
    # # s = wiki.get_source_domain_info(articles['source'])

    # # if articles:
    # return articles ,201