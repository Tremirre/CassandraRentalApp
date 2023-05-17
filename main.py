import os

from rental import app
import dotenv

dotenv.load_dotenv()

CASSANDRA_HOST = os.getenv("CASSANDRA_HOST")
KEYSPACE_NAME = os.getenv("KEYSPACE_NAME")
REPLICATION_FACTOR = int(os.getenv("REPLICATION_FACTOR", 1))


if __name__ == "__main__":
    rent_app = app.RentalApp(
        cassandra_spec={
            "host": [CASSANDRA_HOST],
            "keyspace_name": KEYSPACE_NAME,
            "replication_factor": REPLICATION_FACTOR,
        }
    )
    rent_app.run()
