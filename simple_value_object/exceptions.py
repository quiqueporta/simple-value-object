class SimpleValueObjectException(Exception):
    pass


class InvariantViolation(SimpleValueObjectException):
    pass


class InvariantMustReturnBool(SimpleValueObjectException):
    def __init__(self):
        super().__init__("Invariants must return a boolean value")
