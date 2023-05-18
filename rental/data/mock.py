import json
import random

from pathlib import Path

from cassandra.cqlengine.query import BatchQuery

from . import models
from ..util import chunks

CHUNK_SIZE = 100


def load_mock_data(mock_data_dir: Path) -> None:
    users_data = json.loads((mock_data_dir / "users.json").read_text())
    created_user_ids = []
    for user_batch in chunks(users_data, CHUNK_SIZE):
        with BatchQuery() as batch:
            for user in user_batch:
                new_user = models.User.batch(batch).create(**user)
                created_user_ids.append(new_user.id)

    properties_data = json.loads((mock_data_dir / "properties.json").read_text())

    created_property_ids = []
    for prop_batch in chunks(properties_data, CHUNK_SIZE):
        with BatchQuery() as batch:
            for property in prop_batch:
                new_property = models.RentalProperty.batch(batch).create(**property)
                created_property_ids.append(new_property.id)

    bookings_data = json.loads((mock_data_dir / "bookings.json").read_text())
    booking_users = random.choices(created_user_ids, k=len(bookings_data))
    booking_properties = random.choices(created_property_ids, k=len(bookings_data))

    combined_booking_data = tuple(zip(bookings_data, booking_users, booking_properties))
    for batch_booking_data in chunks(combined_booking_data, CHUNK_SIZE):
        with BatchQuery() as batch:
            for booking, user_id, rental_id in batch_booking_data:
                models.RentalBooking.batch(batch).create(
                    **booking, user_id=user_id, rental_id=rental_id
                )

    reviews_data = json.loads((mock_data_dir / "reviews.json").read_text())
    review_users = random.choices(created_user_ids, k=len(reviews_data))
    review_properties = random.choices(created_property_ids, k=len(reviews_data))

    combined_review_data = tuple(zip(reviews_data, review_users, review_properties))
    for batch_review_data in chunks(combined_review_data, CHUNK_SIZE):
        with BatchQuery() as batch:
            for review, user_id, rental_id in batch_review_data:
                models.RentalReview.batch(batch).create(
                    **review, user_id=user_id, rental_id=rental_id
                )
