import networkx as nx
import json

class GraphMigration:
    def __init__(self, db):
        self.db = db
        self.G = nx.Graph()

    