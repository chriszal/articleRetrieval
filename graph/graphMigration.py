import networkx as nx
import json

class GraphMigration:
    def __init__(self,topics, db):
        self.db = db
        self.topics = topics
        self.G = nx.Graph()

    def create_nodes(self):
        for topic in self.topics:
            cursor_article = self.db[f"{topic}"].find()
            for article in cursor_article:
                self.G.add_node(article["_id"], source=article["source"],article=article['article'], author=article["author"], timestamp=article["timestamp"])

    # def create_edges(self):
