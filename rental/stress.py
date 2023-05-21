import os
import random
import uuid
import multiprocessing as mp

import cassandra.cqlengine.connection as cql_conn

from .data import models, requests


def common_connect(**spec):
    cql_conn.setup(
        spec["hosts"],
        spec["keyspace"],
        retry_connect=True,
    )


def same_request_test(requests_count: int):
    requesting_user = models.User.objects.first()
    if requesting_user is None:
        raise RuntimeError("No users found in database.")
    requesting_user_id = requesting_user.id

    rental_property = models.RentalProperty.objects.first()
    if rental_property is None:
        raise RuntimeError("No rental properties found in database.")
    rental_property_id = rental_property.id

    start_date = "2021-01-01"
    end_date = "2021-01-02"
    for _ in range(requests_count):
        requests.make_reservation(
            user_id=requesting_user_id,
            property_id=rental_property_id,
            start_date=start_date,
            end_date=end_date,
        )


def perform_random_actions(requests_count: int, spec: dict):
    common_connect(**spec)
    requesting_name = f"Test User {os.getpid()}"
    user = models.User.objects.create(name=requesting_name)
    user_id = user.id
    bookings = []
    reviews = []
    all_properties = list(models.RentalProperty.objects.values_list("id"))
    for _ in range(requests_count):
        selection = random.randint(0, 3)
        if selection == 0:
            new_review = requests.add_review(
                user_id=user_id,
                property_id=random.choice(all_properties)[0],
                rating=random.randint(1, 5),
                comment=f"Test comment {random.randint(0, 1000000)}",
            )
            if new_review is not None:
                reviews.append(new_review)
        elif selection == 1:
            year = random.randint(2021, 2024)
            month = random.randint(1, 12)
            day = random.randint(1, 14)
            start_date = f"{year}-{month}-{day}"
            end_date = f"{year}-{month}-{day + random.randint(1, 14)}"
            new_reservation = requests.make_reservation(
                user_id=user_id,
                property_id=random.choice(all_properties)[0],
                start_date=start_date,
                end_date=end_date,
            )
            if new_reservation is not None:
                bookings.append(new_reservation)
        elif selection == 2:
            selected = uuid.uuid4()
            if len(reviews) > 0:
                selected = random.choice(reviews)
            if requests.withdraw_review(selected):
                reviews.remove(selected)
        else:
            selected = uuid.uuid4()
            if len(bookings) > 0:
                selected = random.choice(bookings)
            if requests.cancel_booking(selected):
                bookings.remove(selected)
