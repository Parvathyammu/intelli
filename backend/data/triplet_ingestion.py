from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))


def insert_triplets(triplets):
    with driver.session() as session:
        for t in triplets:
            session.run(
                """
                MERGE (s:Entity {name:$subject})
                MERGE (o:Entity {name:$object})
                MERGE (s)-[:RELATES {type:$predicate}]->(o)
                """,
                subject=t["subject"],
                predicate=t["predicate"],
                object=t["object"]
            )


def clear_graph():
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")


def show_relationships():
    with driver.session() as session:
        result = session.run("""
        MATCH (s:Entity)-[r]->(o:Entity)
        RETURN s.name AS subject, r.type AS predicate, o.name AS object
        """)

        for record in result:
            print(f"{record['subject']} --[{record['predicate']}]--> {record['object']}")


driver.close()