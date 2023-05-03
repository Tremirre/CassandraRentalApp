import typing
import uuid

import cassandra.cluster as cc

ID = typing.TypeVar("ID", uuid.UUID, str, int)
SerializedInstance = typing.TypeVar("SerializedInstance", dict[str, typing.Any])


class CassandraHandler:
    def __init__(self, session: cc.Session, keyspace_name: str):
        self.session = session
        self.keyspace_name = keyspace_name

    def create_keyspace(self, replication_strategy: str) -> None:
        self.session.execute(
            f"CREATE KEYSPACE IF NOT EXISTS {self.keyspace_name} WITH REPLICATION = {replication_strategy};"
        )

    def create_tables(self, table_spec: str) -> None:
        for statement in table_spec.split(";"):
            if statement.strip() != "":
                self.session.execute(statement)

    def initialize(self, replication_strategy: str, table_spec: str) -> None:
        self.create_keyspace(replication_strategy)
        self.session.set_keyspace(self.keyspace_name)
        self.create_tables(table_spec)

    def save(self, table_name: str, data: dict):
        self.session.execute(
            f"INSERT INTO {table_name} ({', '.join(data.keys())}) VALUES ({', '.join(['%s'] * len(data))});",
            tuple(data.values()),
        )

    def get(self, table_name: str, instance_id: ID) -> dict[str, typing.Any]:
        return self.session.execute(
            f"SELECT * FROM {table_name} WHERE id = %s;", (instance_id,)
        ).one()

    def get_all(self, table_name: str) -> list[dict[str, typing.Any]]:
        return self.session.execute(f"SELECT * FROM {table_name};").all()

    def delete(self, table_name: str, instance_id: ID) -> None:
        self.session.execute(f"DELETE FROM {table_name} WHERE id = %s;", (instance_id,))

    def update(self, table_name: str, data: dict, instance_id: ID):
        self.session.execute(
            f"UPDATE {table_name} SET {', '.join([f'{key} = %s' for key in data.keys()])} WHERE id = %s;",
            tuple(data.values()) + (instance_id,),
        )

    def execute_custom(self, query: str) -> list[dict[str, typing.Any]]:
        return self.session.execute(query).all()
