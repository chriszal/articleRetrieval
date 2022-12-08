from mediawiki import MediaWiki

# Init
class MediaWikiApi():
    def __init__(self):
        self.mediawiki = MediaWiki()

    def get_source_domain_info(self,sources):
        source_info={}
        for source in sources:
            article = self.mediawiki.search(source)
            if article:
                source_info[source]=article['description']
        return source_info