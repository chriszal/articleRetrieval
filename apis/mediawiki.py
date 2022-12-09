from mediawiki import MediaWiki

# Init
class MediaWikiApi():
    def __init__(self):
        self.mediawiki = MediaWiki()

    def get_source_domain_info(self,sources):
        source_info={}
        for source in sources:
            articles = self.mediawiki.search(source)
            if articles:
                article = articles[0]
                source_info[source]=article.get('description')
        return source_info