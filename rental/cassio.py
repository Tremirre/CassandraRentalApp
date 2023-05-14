import cassandra.cqlengine.connection as cql_conn
import cassandra.cqlengine.management as cql_mgmt
import cassandra.cqlengine.models as cqlm


class CassandraHandler:
    def __init__(
        self,
        hosts: list[str],
        keyspace: str,
        replication_factor: int = 1,
    ) -> None:
        self.hosts = hosts
        self.keyspace = keyspace
        self.replication_factor = replication_factor
        self.__initialized = False

    def setup(self, models: list[type[cqlm.Model]]) -> None:
        if self.__initialized:
            raise RuntimeError("CassandraHandler already initialized")
        self.__initialized = True
        cql_conn.setup(self.hosts, self.keyspace, retry_connect=True)
        cql_mgmt.create_keyspace_simple(self.keyspace, self.replication_factor)
        for model in models:
            cql_mgmt.sync_table(model)

    def teardown(self) -> None:
        if not self.__initialized:
            raise RuntimeError("CassandraHandler not initialized")
        cql_mgmt.drop_keyspace(self.keyspace)

    def close(self) -> None:
        cql_conn.cluster.shutdown()

    def __del__(self) -> None:
        if self.__initialized and not cql_conn.cluster.is_shutdown:
            self.close()
