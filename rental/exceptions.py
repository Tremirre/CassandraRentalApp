class RentalException(Exception):
    pass


class ValidationException(RentalException):
    pass


class BadValueException(ValidationException):
    pass


class BadTypeException(ValidationException):
    pass


class NonExistentForeignKeyException(ValidationException):
    pass


class ForeignKeyRestrictionViolationException(RentalException):
    pass
