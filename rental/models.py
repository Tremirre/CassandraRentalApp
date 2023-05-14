import typing
import uuid
import dataclasses
import abc
import functools

from . import validators


class ModelMeta(abc.ABCMeta):
    @abc.abstractmethod
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if "__table_name__" not in attrs and not isinstance(cls, abc.ABCMeta):
            raise TypeError(f"{cls.__name__} must have a __table_name__ attribute")


class Model(abc.ABC, metaclass=ModelMeta):
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
    name: str
    description: str
    address: str
    bedrooms: int
    bathrooms: int
    price: float
    id: uuid.UUID = dataclasses.field(default_factory=uuid.uuid4)
    __table_name__: typing.ClassVar[str] = dataclasses.field(
        init=False, default="rental_properties"
    )

    validators = [
        functools.partial(validators.validate_non_negative, field_name="bedrooms"),
        functools.partial(validators.validate_non_negative, field_name="bathrooms"),
        functools.partial(validators.validate_non_negative, field_name="price"),
        functools.partial(validators.validate_non_empty, field_name="name"),
    ]


@dataclasses.dataclass
class RentalBooking(Model):
    start_date: str
    end_date: str
    rental_id: uuid.UUID
    user_id: uuid.UUID
    id: uuid.UUID = dataclasses.field(default_factory=uuid.uuid4)
    __table_name__: typing.ClassVar[str] = dataclasses.field(
        init=False, default="rental_bookings"
    )

    validators = [
        functools.partial(validators.validate_non_empty, field_name="start_date"),
        functools.partial(validators.validate_non_empty, field_name="end_date"),
    ]


@dataclasses.dataclass
class RentalReview(Model):
    rental_id: uuid.UUID
    user_id: uuid.UUID
    rating: int
    comment: str
    id: uuid.UUID = dataclasses.field(default_factory=uuid.uuid4)
    __table_name__: typing.ClassVar[str] = dataclasses.field(
        init=False, default="rental_reviews"
    )

    validators = [
        functools.partial(validators.validate_non_empty, field_name="comment"),
        functools.partial(
            validators.validate_in_range, field_name="rating", min_value=1, max_value=5
        ),
    ]


@dataclasses.dataclass
class User(Model):
    name: str
    id: uuid.UUID = dataclasses.field(default_factory=uuid.uuid4)
    __table_name__: typing.ClassVar[str] = dataclasses.field(
        init=False, default="users"
    )

    validators = [
        functools.partial(validators.validate_non_empty, field_name="name"),
    ]
