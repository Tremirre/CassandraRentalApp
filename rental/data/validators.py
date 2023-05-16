import typing

import cassandra.cqlengine.models as cqlm

from .. import exceptions


def validate_non_negative(model_instance: cqlm.Model, field_name: str):
    value = getattr(model_instance, field_name)
    if value is None:
        return
    try:
        if value < 0:
            raise exceptions.BadValueException(f"{field_name} must be non-negative")
    except TypeError:
        raise exceptions.BadTypeException(f"{field_name} must be a number")


def validate_non_empty(model_instance: cqlm.Model, field_name: str):
    value = getattr(model_instance, field_name)
    if value == "" or value is None:
        raise exceptions.BadValueException(f"{field_name} must be non-empty")


def validate_in_range(
    model_instance: cqlm.Model, field_name: str, min_value: int, max_value: int
):
    value = getattr(model_instance, field_name)
    if value is None:
        return
    try:
        if value < min_value or value > max_value:
            raise exceptions.BadValueException(
                f"{field_name} must be between {min_value} and {max_value}"
            )
    except TypeError:
        raise exceptions.BadTypeException(f"{field_name} must be a number")


def validate_foreign_key(
    model_instance: cqlm.Model,
    field_name: str,
    ref_model: typing.Type[cqlm.Model],
    ref_field: str = "id",
):
    value = getattr(model_instance, field_name)
    if value is None:
        return
    if not ref_model.objects(**{ref_field: value}).count():
        raise exceptions.NonExistentForeignKeyException(
            f"Instance of {ref_model} with {ref_field}={value} does not exist"
        )
