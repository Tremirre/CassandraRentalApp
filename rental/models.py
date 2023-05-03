import typing
import uuid
import dataclasses
import abc
import functools

from . import validators


class Model(abc.ABC):
    __table_name__: typing.ClassVar[str]

    def __init__(self):
        if not hasattr(self, "validators"):
            self.validators = []

    def validate(self) -> None:
        for validator in self.validators:
            validator(self)

    def to_dict(self) -> dict[str, typing.Any]:
        return dataclasses.asdict(self)

    def __post_init__(self):
        super().__init__()
        self.validate()


@dataclasses.dataclass
class RentalProperty(Model):
    id: uuid.UUID = dataclasses.field(default_factory=uuid.uuid4)
    name: str
    description: str
    address: str
    bedrooms: int
    bathrooms: int
    price: float
    __table_name__: typing.ClassVar[str] = "rental_properties"

    validators = [
        functools.partial(validators.validate_non_negative, field_name="bedrooms"),
        functools.partial(validators.validate_non_negative, field_name="bathrooms"),
        functools.partial(validators.validate_non_negative, field_name="price"),
        functools.partial(validators.validate_non_empty, field_name="name"),
    ]


@dataclasses.dataclass
class RentalBooking(Model):
    id: uuid.UUID = dataclasses.field(default_factory=uuid.uuid4)
    rental_id: uuid.UUID
    start_date: str
    end_date: str
    user_id: uuid.UUID
    __table_name__: typing.ClassVar[str] = "rental_bookings"

    validators = [
        functools.partial(validators.validate_non_empty, field_name="start_date"),
        functools.partial(validators.validate_non_empty, field_name="end_date"),
    ]


@dataclasses.dataclass
class RentalReview(Model):
    id: uuid.UUID = dataclasses.field(default_factory=uuid.uuid4)
    rental_id: uuid.UUID
    user_id: uuid.UUID
    rating: int
    comment: str
    __table_name__: typing.ClassVar[str] = "rental_reviews"

    validators = [
        functools.partial(validators.validate_non_empty, field_name="comment"),
        functools.partial(
            validators.validate_in_range, field_name="rating", min_value=1, max_value=5
        ),
    ]


@dataclasses.dataclass
class User(Model):
    id: uuid.UUID = dataclasses.field(default_factory=uuid.uuid4)
    name: str
    __table_name__: typing.ClassVar[str] = "users"

    validators = [
        functools.partial(validators.validate_non_empty, field_name="name"),
    ]
