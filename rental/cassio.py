import cassandra.cqlengine.connection as cql_conn
import cassandra.cqlengine.management as cql_mgmt
import cassandra.cqlengine.models as cqlm
import cassandra.cqlengine.query as cql_query

from typing import Callable

from rental.util import chunks


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

    def setup(
        self,
        models: list[type[cqlm.Model]],
        progress_callback: Callable[[float, str], None] = lambda *x: None,
    ) -> None:
        if self.__initialized:
            raise RuntimeError("CassandraHandler already initialized")
        self.__initialized = True
        progress_callback(5, "Connecting to Cassandra")
        cql_conn.setup(self.hosts, self.keyspace, retry_connect=True)
        progress_callback(20, "Creating keyspace")
        cql_mgmt.create_keyspace_simple(self.keyspace, self.replication_factor)
        len_models = len(models)
        for i, model in enumerate(models):
            progress_callback(
                40 + 60 * (i + 1) / len_models, f"Syncing {model.__name__}"
            )
            cql_mgmt.sync_table(model)

    def teardown(self) -> None:
        if not self.__initialized:
            raise RuntimeError("CassandraHandler not initialized")
        cql_mgmt.drop_keyspace(self.keyspace)

    def clear_tables(self, models: list[type[cqlm.Model]], safe: bool = True) -> None:
        if not self.__initialized:
            raise RuntimeError("CassandraHandler not initialized")

        if not safe:
            for model in models:
                cql_conn.session.execute(
                    f"TRUNCATE {self.keyspace}.{model._table_name}"
                )
            return

        for model in models:
            all_objects = model.objects.all()
            for model_batch in chunks(all_objects, 100):
                with cql_query.BatchQuery() as batch:
                    for obj in model_batch:
                        obj.batch(batch).delete()

    def close(self) -> None:
        cql_conn.cluster.shutdown()

    def __del__(self) -> None:
        if self.__initialized and not cql_conn.cluster.is_shutdown:
            self.close()
