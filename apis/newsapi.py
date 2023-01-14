import requests


# Init
class NewsApi():
    def __init__(self):
        self.secret = "420d1582b00240789d9fc79e7943e61f"

    def get_articles(self, keyword):
        response = requests.get("https://newsapi.org/v2/everything",
                                params={'q': keyword, 'apiKey': self.secret, 'language': 'en'})
        if response.status_code == 200:
            response_dict = response.json()
            articles = []

            for article in response_dict['articles']:
                source = article['source']['name']
                articles.append({'source': source, 'article': article['content']})

            if not articles:
                articles = [{'source': '', 'article': ''}]
            return articles
        else:
            return [{'source': '', 'article': ''}]

    #     articles =[]
    # for keyword in keywords:
    #     articles.append(news.get_articles(keyword))
    #     # sources.get_source_domain_info(articles['source'])
    # # s = wiki.get_source_domain_info(articles['source'])

    # # if articles:
    # return articles ,201
