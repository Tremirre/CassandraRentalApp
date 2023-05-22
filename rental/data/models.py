from __future__ import annotations

import typing
import uuid
import functools

import cassandra.cqlengine.models as cqlm
import cassandra.cqlengine.columns as cql_columns

from .. import exceptions
from . import validators, columns


class _IdentifieableValidatedModel(cqlm.Model):
    class FKRegistryEntry(typing.NamedTuple):
        field_name: str
        ref_model: typing.Type[cqlm.Model]
        on_delete: columns.OnDelete

    id: uuid.UUID = cql_columns.UUID(primary_key=True, default=uuid.uuid4)
    validators: list[typing.Callable] = []
    unique_field_groups: list[tuple[str]] = []
    reffed_by: list[FKRegistryEntry] | None = None

    @classmethod
    def register_external_foreign_key(
        cls,
        field_name: str,
        ref_model: typing.Type[cqlm.Model],
        on_delete: columns.OnDelete,
    ) -> None:
        if cls.reffed_by is None:
            cls.reffed_by = []
        cls.reffed_by.append(
            _IdentifieableValidatedModel.FKRegistryEntry(
                field_name=field_name, ref_model=ref_model, on_delete=on_delete
            )
        )

    @classmethod
    def register_internal_foreign_keys(cls) -> None:
        for column_name, column_spec in cls._columns.items():
            if isinstance(column_spec, columns.ForeignUUID):
                column_spec.ref_model.register_external_foreign_key(
                    field_name=column_name,
                    ref_model=cls,
                    on_delete=column_spec.on_delete,
                )

    def validate(self) -> None:
        for validator in self.validators:
            validator(self)
        for field_group in self.unique_field_groups:
            relevant_qs = self.objects.filter(
                **{field_name: getattr(self, field_name) for field_name in field_group}
            ).allow_filtering()
            allowable_count = 0
            if self.objects.filter(id=self.id).count():
                allowable_count = 1
            if relevant_qs.count() > allowable_count:
                raise exceptions.UniqueFieldsRestrictionViolationException(
                    "An object with the same values for the following fields already exists: "
                    + ", ".join(field_group)
                )

    def save(self):
        self.validate()
        return super().save()

    def resolve_fk_cascade(self):
        if self.reffed_by is None:
            return
        for entry in self.reffed_by:
            ref_qs = entry.ref_model.objects(**{entry.field_name: self.id})
            if not ref_qs.count():
                continue
            if entry.on_delete == columns.OnDelete.CASCADE:
                for ref in ref_qs:
                    ref.delete()

            elif entry.on_delete == columns.OnDelete.SET_NULL:
                for ref in ref_qs:
                    ref.update(**{entry.field_name: None})

            elif entry.on_delete == columns.OnDelete.RESTRICT:
                raise exceptions.ForeignKeyRestrictionViolationException(
                    f"Instance of {entry.ref_model} with {entry.field_name}={self.id} exists"
                )

            else:
                raise ValueError(f"Unknown OnDelete value: {entry.on_delete}")

    def delete(self):
        self.resolve_fk_cascade()
        return super().delete()


class RentalProperty(_IdentifieableValidatedModel):
    name: str = cql_columns.Text(required=True, index=True)
    description: str = cql_columns.Text()
    address: str = cql_columns.Text(required=True)
    bedrooms: int = cql_columns.Integer(required=True, default=0)
    bathrooms: int = cql_columns.Integer(required=True, default=0)
    price_per_night: float = cql_columns.Float(required=True)

    validators = [
        functools.partial(validators.validate_non_negative, field_name="bedrooms"),
        functools.partial(validators.validate_non_negative, field_name="bathrooms"),
        functools.partial(
            validators.validate_non_negative, field_name="price_per_night"
        ),
        functools.partial(validators.validate_non_empty, field_name="name"),
    ]


class User(_IdentifieableValidatedModel):
    name: str = cql_columns.Text(required=True, index=True)


class RentalBooking(_IdentifieableValidatedModel):
    start_date: str = cql_columns.Date(required=True)
    end_date: str = cql_columns.Date(required=True)
    rental_id: uuid.UUID = columns.ForeignUUID(
        required=True,
        ref_model=RentalProperty,
        on_delete=columns.OnDelete.CASCADE,
    )
    user_id: uuid.UUID = columns.ForeignUUID(
        required=True,
        ref_model=User,
        on_delete=columns.OnDelete.CASCADE,
    )

    def validate_no_overlapping_bookings(self):
        overlapping_qs = self.objects.filter(
            rental_id=self.rental_id,
            start_date__lte=self.end_date,
            end_date__gte=self.start_date,
        ).allow_filtering()
        external_overlapping = [
            booking for booking in overlapping_qs if booking.id != self.id
        ]
        if external_overlapping:
            raise exceptions.OverlappingBookingException(
                "This booking overlaps with an existing booking"
            )

    def validate_start_date_before_end_date(self):
        if self.start_date > self.end_date:
            raise exceptions.BadValueException("Start date must be before end date")

    validators = [
        functools.partial(validators.validate_non_empty, field_name="start_date"),
        functools.partial(validators.validate_non_empty, field_name="end_date"),
        validate_no_overlapping_bookings,
        validate_start_date_before_end_date,
    ]

    unique_field_groups = [("rental_id", "user_id")]


class RentalReview(_IdentifieableValidatedModel):
    rating: int = cql_columns.Integer(required=True)
    comment: str = cql_columns.Text(required=False)
    rental_id: uuid.UUID = columns.ForeignUUID(
        required=True, ref_model=RentalProperty, on_delete=columns.OnDelete.CASCADE
    )
    user_id: uuid.UUID = columns.ForeignUUID(
        required=False, ref_model=User, on_delete=columns.OnDelete.SET_NULL
    )

    validators = [
        functools.partial(
            validators.validate_in_range, field_name="rating", min_value=1, max_value=5
        ),
    ]

    unique_field_groups = [("rental_id", "user_id")]


MODELS = [cls for cls in _IdentifieableValidatedModel.__subclasses__()]
for model in MODELS:
    model.register_internal_foreign_keys()
