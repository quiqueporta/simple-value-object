class ConstructorWithoutArguments(Exception):
    def __init__(self):
        super().__init__('No arguments declared in __init__')


class CannotBeChanged(Exception):
    def __init__(self):
        super().__init__(
            'You cannot change values from a Value Object, create a new one'
        )


class InvariantViolation(Exception):
    pass


class InvariantMustReturnBool(Exception):
    def __init__(self):
        super().__init__('Invariants must return a boolean value')
