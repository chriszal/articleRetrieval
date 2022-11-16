from mediawiki import MediaWiki

# Init
class MediaWikiApi():
    def __init__(self):
        self.mediawiki = MediaWiki()

    def get_page_from_domain(self,domain_name):
        return self.mediawiki.search(domain_name)