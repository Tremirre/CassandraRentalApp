import os
import random
import uuid

import cassandra.cqlengine.connection as cql_conn

from datetime import datetime, timedelta

from .data import models, requests
from .util import random_date


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

    start_date = random_date()
    end_date = start_date + timedelta(days=random.randint(1, 14))
    for _ in range(requests_count):
        requests.make_reservation(
            user_id=requesting_user_id,
            property_id=rental_property_id,
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
        )


def perform_random_actions(requests_count: int, spec: dict):
    common_connect(**spec)
    requesting_name = f"Stress Test 2 User {os.getpid()}"
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
            start_date = random_date()
            end_date = start_date + timedelta(days=random.randint(1, 28))
            new_reservation = requests.make_reservation(
                user_id=user_id,
                property_id=random.choice(all_properties)[0],
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d"),
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


def occupy_all(spec: dict):
    common_connect(**spec)
    user = models.User.objects.create(name=f"Stress Test 3 User {os.getpid()}")
    all_properties = list(models.RentalProperty.objects.values_list("id"))
    random.shuffle(all_properties)
    start_date = datetime.now()
    end_date = start_date + timedelta(days=14)
    for property_id in all_properties:
        requests.make_reservation(
            user_id=user.id,
            property_id=property_id[0],
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
        )


def occupy_cancel_freq(requests_count: int, spec: dict):
    common_connect(**spec)
    user = models.User.objects.create(name=f"Stress Test 4 User {os.getpid()}")
    all_properties = list(models.RentalProperty.objects.values_list("id"))
    random.shuffle(all_properties)
    made_bookings = []
    for _ in range(requests_count):
        if made_bookings and random.random() < 0.5:
            selected = random.choice(made_bookings)
            is_cancelled = requests.cancel_booking(selected)
            if is_cancelled:
                made_bookings.remove(selected)
        else:
            selected = random.choice(all_properties)
            start_date = random_date()
            end_date = start_date + timedelta(days=random.randint(1, 28))
            new_booking = requests.make_reservation(
                user_id=user.id,
                property_id=selected[0],
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d"),
            )
            if new_booking is not None:
                made_bookings.append(new_booking)
