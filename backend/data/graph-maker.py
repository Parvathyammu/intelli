from neo4j import GraphDatabase
from pyvis.network import Network
from dotenv import load_dotenv
import os

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))


def build_graph():
    net = Network(directed=True)

    with driver.session() as session:
        result = session.run(
            "MATCH (n)-[r]->(m) RETURN n.name AS source, type(r) AS rel, m.name AS target"
        )

        for record in result:
            net.add_node(record["source"], color="#c27aff")
            net.add_node(record["target"], color="#c27aff")
            net.add_edge(record["source"], record["target"], label=record["rel"])

    return net


def save_graph(net):
    net.save_graph("neo4j_graph.html")
    print("Graph saved as neo4j_graph.html")


if __name__ == "__main__":
    graph = build_graph()
    save_graph(graph)