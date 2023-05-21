import os
import dotenv

from rental.stress import occupy_cancel_freq

dotenv.load_dotenv()
occupy_cancel_freq(
    100,
    {"hosts": [os.getenv("CASSANDRA_HOST")], "keyspace": os.getenv("KEYSPACE_NAME")},
)
