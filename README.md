# CassandraRentalApp

A simple GUI app for managing fictional rentals with Cassandra cluster as the data layer.

Requires `python3.10` or higher.

## Starting the app

A precondition to start RentalApp is to setup a cassandra cluster and specify its params as environmemt variables.
The provided `docker-compose.yaml` file allows to start up 3 cassandra nodes with a command

> docker-compose up

After Cassandra has started, the connection variables need to be specified:

- CASSANDRA_HOST: IP adress of the cluster
- KEYSPACE_NAME: name of the keyspace to use
- REPLICATION_FACTOR: replication factor of the keyspace

Nextly, the requirements have to be installed using pip:

> pip install -r requirements.txt

Finally, to start the application input the following command:

> python main.py
