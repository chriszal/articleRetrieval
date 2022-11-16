from newsapi import NewsApiClient

# Init
class NewsApi():
    def __init__(self):
        self.newsapi = NewsApiClient(api_key='420d1582b00240789d9fc79e7943e61f')
        self.topics=["motorsport","agriculture","war"]

    def get_articles(self):
        for topic in self.topics:
            top_headlines = self.newsapi.get_top_headlines(q=topic)
            Headlines = top_headlines['articles']
            
            # now we will display the that news with a good readability for user
            if Headlines:
                    for articles in Headlines:
                        b = articles['title'][::-1].index("-")
                        if "news" in (articles['title'][-b+1:]).lower():
                            print(str(articles['title'][-b+1:])+":"+ str(articles['title'][:-b-2]))
                        else:
                            print(str(articles['title'][-b+1:])+" News: "+str(articles['title'][:-b-2]))
            else:
                print("Sorry no articles found for "+str(topic)+", Something Wrong!!!")
