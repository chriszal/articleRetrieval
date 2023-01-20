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
                            str(article["_id"])
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

        #getting all the nodeId's
        list_of_nodes = list(self.G.nodes)

        #Getting all the nodes because if we add one search for each node we are going to destroy our database and the result would take super long.
        articles_obj_list = self.db.fetch_all_articles()["data"]

        #Looping over node id's
        for node in list_of_nodes:

            article_match = next((x for x in articles_obj_list if x["id"] == node), None)

            if article_match is None:
                continue

            timestamp = int(article_match["timestamp"])
            source = str(article_match["source"])
            author = str(article_match["author"])

            # This is a faster way to loop over a large number of elements
            # candidates_to_add_edges = [node_id for node_id in list_of_nodes if
            # (source == G.nodes[node_id]["source"] or author == G.nodes[node_id]["author"])]

            cnt = True
            self.G.add_node(0, timestamp=-1, node="a0")
            # Looping over candidate node id's


            for node_id in list_of_nodes:
                article_match_2 = next((x for x in articles_obj_list if x["id"] == node_id), None)

                if article_match_2 is None:
                    continue
                #We avoind creating self loops
                if node == node_id:
                    continue

                # Not the best metric on the planet though....!
                if (abs(timestamp - int(article_match_2["timestamp"]))) < self.G.nodes[0]["timestamp"]:
                    self.G.nodes[0]["node"] = node_id
                    self.G.nodes[0]["timestamp"] = abs(timestamp - int(article_match_2["timestamp"]))

                # Here we take the case where we have the same source in order to create an edge between the two nodes
                if source == article_match_2["source"]:
                    self.G.add_edge(node, node_id, source=source)
                    cnt = False
                    continue  # we jump straight to the next iteration

                # Here we take the case where we have the same author in order to create an edge between the two nodes
                if author == article_match_2["author"]:
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

