from threading import Timer

import networkx as nx
import json


class GraphMigration:

    def __init__(self, db, topics=["education",
                                   "health",
                                   "business",
                                   "motorsport",
                                   "science",
                                   "space",
                                   "technology",
                                   "war"]):
        self.topics = topics
        self.db = db
        # Creating a new graph
        self.G = nx.Graph()


    def get_graph(self):
        return self.G

    def set_graph(self, ready_graph):
        self.G = ready_graph

    def create_nodes(self):
        for topic in self.topics:
            cursor_article = self.db.find_articles_from_topic(topic)
            for article in cursor_article:
                if not self.G.has_node(str(article["_id"])):
                    self.G.add_nodes_from([
                        (
                            str(article["_id"]),
                            {"source": str(article["source"]), "article": str(article['article']),
                             "author": str(article["author"]), "timestamp": int(article["timestamp"])}
                        )
                    ])

    #TODO-Optimize it....maybe not updating again the hole thing of edges???!?!?!!?
    def update_graph(self):
        #Here we are creating the new nodes
        self.create_nodes()
        #here we are creating all the edges again,
        '''
            Adding an edge that already exists updates the edge data. 
            Many NetworkX algorithms designed for weighted graphs use an edge 
            attribute (by default weight )
        '''
        self.create_edges()

    def create_edges(self):

        list_of_nodes = list(self.G.nodes)
        for node in list_of_nodes:
            timestamp = self.G.nodes[node]["timestamp"]
            source = self.G.nodes[node]["source"]
            author = self.G.nodes[node]["author"]

            # This is a faster way to loop over a large number of elements
            # candidates_to_add_edges = [node_id for node_id in list_of_nodes if
            #                            (source == G.nodes[node_id]["source"] or author == G.nodes[node_id]["author"])]

            cnt = True
            self.G.add_node(0, timestamp=-1, node="a0")
            for node_id in list_of_nodes:

                #We avoind creating self loops
                if node == node_id:
                    continue

                # Not the best metric on the planet though....!
                if (abs(timestamp - self.G.nodes[node_id]["timestamp"])) < self.G.nodes[0]["timestamp"]:
                    self.G.nodes[0]["node"] = node_id
                    self.G.nodes[0]["timestamp"] = abs(timestamp - self.G.nodes[node_id]["timestamp"])

                # Here we take the case where we have the same source in order to create an edge between the two nodes
                if source == self.G.nodes[node_id]["source"]:
                    self.G.add_edge(node, node_id, source=source)
                    cnt = False
                    continue  # we jump straight to the next iteration

                # Here we take the case where we have the same author in order to create an edge between the two nodes
                if author == self.G.nodes[node_id]["author"]:
                    self.G.add_edge(node, node_id, author=author)
                    cnt = False
                    continue  # we jump straight to the next iteration

            # Now we take the case where we have not created any edges betweeen any nodes because we did not have either,
            # 1. Same sources
            # 2. Same authors
            # (Extremely rare case)
            if cnt:
                self.G.add_edge(node, self.G.nodes[0]["node"], timestamp=self.G.nodes[0]["timestamp"])


    def automatic_updater(self):
        # caling the right function in order to update the graph
        self.update_graph()

        # Use a timer to schedule the next API call in seconds
        timer = Timer(64800, self.automatic_updater)
        timer.start()

