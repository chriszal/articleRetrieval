from mediawiki import MediaWiki

# Init
class MediaWikiApi():
    def __init__(self):
        self.mediawiki = MediaWiki()

    def get_source_domain_info(self,sources):
        source_info = {}
        for source in sources:
            # Search for articles with the source domain name
            articles = self.mediawiki.search(source)

            # Add the list of articles to the source_info dictionary
            source_info[source] = articles
        return source_info