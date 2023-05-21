from uuid import UUID

from cassandra.cqlengine.models import _DoesNotExist

from . import models


def make_reservation(
    user_id: UUID,
    property_id: UUID,
    start_date: str,
    end_date: str,
    ignore_errors: bool = True,
) -> UUID | None:
    booking = models.RentalBooking(
        user_id=user_id,
        rental_id=property_id,
        start_date=start_date,
        end_date=end_date,
    )
    if ignore_errors:
        try:
            booking.save()
        except models.exceptions.OverlappingBookingException:
            return None
        except models.exceptions.UniqueFieldsRestrictionViolationException:
            return None
    else:
        booking.save()
    return booking.id


def add_review(
    user_id: UUID,
    property_id: UUID,
    rating: int,
    comment: str,
    ignore_errors: bool = True,
) -> UUID:
    review = models.RentalReview(
        user_id=user_id,
        rental_id=property_id,
        rating=rating,
        comment=comment,
    )
    if ignore_errors:
        try:
            review.save()
        except models.exceptions.BadValueException:
            return None
        except models.exceptions.UniqueFieldsRestrictionViolationException:
            return None
    else:
        review.save()
    return review.id


def cancel_booking(booking_id: UUID) -> bool:
    try:
        booking = models.RentalBooking.objects.get(id=booking_id)
    except _DoesNotExist:
        return False
    booking.delete()
    return True


def withdraw_review(review_id: UUID) -> bool:
    try:
        review = models.RentalReview.objects.get(id=review_id)
    except _DoesNotExist:
        return False
    review.delete()
    return True
