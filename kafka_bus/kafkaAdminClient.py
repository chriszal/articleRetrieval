from kafka.admin import KafkaAdminClient, NewTopic



class KafkaAdminThread:
    def __init__(self,topics):
        self.topics = topics

    def start(self):
        admin_client = KafkaAdminClient(
            bootstrap_servers=['kafka:29092'], 
                client_id='my_client'
        )
        topic_list = []
        for topic in self.topics:
            topic_list.append(NewTopic(name=topic, num_partitions=1, replication_factor=1))
        admin_client.create_topics(new_topics=topic_list, validate_only=False)