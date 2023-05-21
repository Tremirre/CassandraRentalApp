import os
import dotenv

from rental.stress import perform_random_actions

dotenv.load_dotenv()
perform_random_actions(
    100,
    {"hosts": [os.getenv("CASSANDRA_HOST")], "keyspace": os.getenv("KEYSPACE_NAME")},
)
