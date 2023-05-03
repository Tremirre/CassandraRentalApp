import typing


def validate_non_negative(model: typing.Any, field_name: str):
    if getattr(model, field_name) < 0:
        raise ValueError(f"{field_name} must be non-negative")


def validate_non_empty(model: typing.Any, field_name: str):
    value = getattr(model, field_name)
    if value == "" or value is None:
        raise ValueError(f"{field_name} must be non-empty")


def validate_in_range(
    model: typing.Any, field_name: str, min_value: int, max_value: int
):
    value = getattr(model, field_name)
    if value < min_value or value > max_value:
        raise ValueError(f"{field_name} must be between {min_value} and {max_value}")
