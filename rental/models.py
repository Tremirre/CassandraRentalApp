from __future__ import annotations

import typing
import uuid
import functools

import cassandra.cqlengine.models as cqlm
import cassandra.cqlengine.columns as cql_columns

from . import validators


class _IdentifieableValidatedModel(cqlm.Model):
    id: uuid.UUID = cql_columns.UUID(primary_key=True, default=uuid.uuid4)
    validators: list[typing.Callable] = []

    def validate(self) -> None:
        for validator in self.validators:
            validator(self)

    def save(self):
        self.validate()
        return super().save()


class RentalProperty(_IdentifieableValidatedModel):
    name: str = cql_columns.Text(required=True, index=True)
    description: str = cql_columns.Text()
    address: str = cql_columns.Text(required=True)
    bedrooms: int = cql_columns.Integer(required=True, default=0)
    bathrooms: int = cql_columns.Integer(required=True, default=0)
    price: float = cql_columns.Float(required=True)

    validators = [
        functools.partial(validators.validate_non_negative, field_name="bedrooms"),
        functools.partial(validators.validate_non_negative, field_name="bathrooms"),
        functools.partial(validators.validate_non_negative, field_name="price"),
        functools.partial(validators.validate_non_empty, field_name="name"),
    ]


class User(_IdentifieableValidatedModel):
    name: str = cql_columns.Text(required=True)


class RentalBooking(_IdentifieableValidatedModel):
    start_date: str = cql_columns.Date(required=True)
    end_date: str = cql_columns.Date(required=True)
    rental_id: uuid.UUID = cql_columns.UUID(required=True)
    user_id: uuid.UUID = cql_columns.UUID(required=True)

    validators = [
        functools.partial(validators.validate_non_empty, field_name="start_date"),
        functools.partial(validators.validate_non_empty, field_name="end_date"),
        functools.partial(
            validators.validate_foreign_key,
            field_name="rental_id",
            ref_model=RentalProperty,
        ),
        functools.partial(
            validators.validate_foreign_key, field_name="user_id", ref_model=User
        ),
    ]


class RentalReview(_IdentifieableValidatedModel):
    rental_id: uuid.UUID = cql_columns.UUID(required=True)
    user_id: uuid.UUID = cql_columns.UUID(required=True)
    rating: int = cql_columns.Integer(required=True)
    comment: str = cql_columns.Text(required=False)

    validators = [
        functools.partial(
            validators.validate_in_range, field_name="rating", min_value=1, max_value=5
        ),
        functools.partial(
            validators.validate_foreign_key,
            field_name="rental_id",
            ref_model=RentalProperty,
        ),
        functools.partial(
            validators.validate_foreign_key, field_name="user_id", ref_model=User
        ),
    ]


MODELS = [cls for cls in _IdentifieableValidatedModel.__subclasses__()]
