import os

import dotenv
import cassandra.cluster as cc
import cassandra.query as cq

dotenv.load_dotenv()

KEYSPACE_NAME = "house_rentals"
CASSANDRA_HOST = os.getenv("CASSANDRA_HOST")
NUM_NODES = int(os.getenv("NUM_NODES"))


def setup_keyspace(
    session: cc.Session,
    num_nodes: int,
    keyspace_name: str,
) -> None:
    replication_strategy = (
        "{{ 'class' : 'SimpleStrategy', 'replication_factor' : {num_nodes} }}".format(
            num_nodes=num_nodes
        )
    )
    session.execute(
        f"CREATE KEYSPACE IF NOT EXISTS {keyspace_name} WITH REPLICATION = {replication_strategy};"
    )


def main():
    cluster = cc.Cluster(
        [CASSANDRA_HOST],
        port=9042,
    )
    session = cluster.connect()

    setup_keyspace(session, NUM_NODES, KEYSPACE_NAME)
    session.set_keyspace(KEYSPACE_NAME)

    with open("create_tables.cql", "r") as f:
        all_statements = f.read()

    for statement in all_statements.split(";"):
        if statement.strip() != "":
            session.execute(statement)

    cluster.shutdown()


if __name__ == "__main__":
    main()
