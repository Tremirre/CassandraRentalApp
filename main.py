import os
import dotenv

from pathlib import Path

from rental import app

dotenv.load_dotenv()

CASSANDRA_HOST = os.getenv("CASSANDRA_HOST")
KEYSPACE_NAME = os.getenv("KEYSPACE_NAME")
REPLICATION_FACTOR = int(os.getenv("REPLICATION_FACTOR", 1))

MOCK_DATA_DIR = Path(__file__).parent / "mockdata_s"

if __name__ == "__main__":
    rent_app = app.RentalApp(
        cassandra_spec={
            "hosts": [CASSANDRA_HOST],
            "keyspace": KEYSPACE_NAME,
            "replication_factor": REPLICATION_FACTOR,
        }
    )
    rent_app.set_mock_data_dir(MOCK_DATA_DIR)
    rent_app.run()
