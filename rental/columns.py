from __future__ import annotations
import typing
import uuid
import enum

import cassandra.cqlengine.columns as cql_columns
import cassandra.cqlengine.models as cqlm
import cassandra.cqlengine.query as cql_query

from . import exceptions


class OnDelete(enum.Enum):
    CASCADE = "CASCADE"
    RESTRICT = "RESTRICT"
    SET_NULL = "SET NULL"


class _Model(typing.Protocol):
    pk: uuid.UUID
    objects: cql_query.ModelQuerySet

    @classmethod
    def register_external_foreign_key(
        cls,
        field_name: str,
        ref_model: typing.Type[cqlm.Model],
        on_delete: OnDelete,
    ) -> None:
        ...


class ForeignUUID(cql_columns.UUID):
    def __init__(
        self,
        *args,
        ref_model: typing.Type[_Model],
        on_delete: OnDelete = OnDelete.RESTRICT,
        **kwargs,
    ):
        super().__init__(*args, **kwargs, index=True)
        self.ref_model = ref_model
        self.on_delete = on_delete

    def validate(self, value: uuid.UUID) -> uuid.UUID:
        id_field = self.ref_model.pk.column.column_name
        if not self.ref_model.objects(**{id_field: value}).count():
            raise exceptions.NonExistentForeignKeyException(
                f"Instance of {self.ref_model} with {id_field}={value} does not exist"
            )
        return super().validate(value)
