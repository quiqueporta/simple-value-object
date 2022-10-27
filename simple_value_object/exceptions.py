class SimpleValueObjectException(Exception):
    pass


class ConstructorWithoutArguments(SimpleValueObjectException):
    def __init__(self):
        super().__init__('No arguments declared in __init__')


class CannotBeChanged(SimpleValueObjectException):
    def __init__(self):
        super().__init__(
            'You cannot change values from a Value Object, create a new one'
        )


class InvariantViolation(SimpleValueObjectException):
    pass


class InvariantMustReturnBool(SimpleValueObjectException):
    def __init__(self):
        super().__init__('Invariants must return a boolean value')
