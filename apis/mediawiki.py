from mediawiki import MediaWiki, DisambiguationError, PageError

# Init
class MediaWikiApi():
    def __init__(self):
        self.mediawiki = MediaWiki()

    def get_source_domain_info(self, source_name):
        # Search for articles with the source domain name
        try:
            articles = self.mediawiki.page(source_name)
        except DisambiguationError as e:
            # Handle the case where multiple pages are found
            return e.options
        except PageError as e:
            return e.message
        else:
            # Return the first article's description
            return articles.summary