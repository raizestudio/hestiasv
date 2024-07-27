from elasticsearch import Elasticsearch

ELASTIC_PASSWORD = "formation"
ELASTIC_HOST = "localhost"
ELASTIC_PORT = 9200


def get_elk_client():
    return Elasticsearch(
        hosts=[f"http://{ELASTIC_HOST}:{ELASTIC_PORT}"],
        basic_auth=("elastic", ELASTIC_PASSWORD),
    )


# Test the connection
print(get_elk_client().info())
