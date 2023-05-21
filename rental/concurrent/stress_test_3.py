import os
import dotenv

from rental.stress import occupy_all

dotenv.load_dotenv()
occupy_all(
    {"hosts": [os.getenv("CASSANDRA_HOST")], "keyspace": os.getenv("KEYSPACE_NAME")},
)
