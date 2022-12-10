from mediawiki import MediaWiki

# Init
class MediaWikiApi():
    def __init__(self):
        self.mediawiki = MediaWiki()

    def get_source_domain_info(self, source_name):
        # Search for articles with the source domain name
        articles = self.mediawiki.page(source_name)

        # Return the first article's description
        return articles.summary