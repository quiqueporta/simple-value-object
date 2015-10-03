class NotDeclaredArgsException(Exception):
    def __init__(self, *args, **kwargs):
        super(NotDeclaredArgsException, self).__init__(
            'No arguments declared in __init__'
        )


class ArgWithoutValueException(Exception):
    pass


class CannotBeChangeException(Exception):
    def __init__(self, *args, **kwargs):
        super(CannotBeChangeException, self).__init__(
            'You cannot change values from a Value Object, create a new one'
        )


class ViolatedInvariantException(Exception):
    pass


class InvariantReturnValueException(Exception):
    def __init__(self, *args, **kwargs):
        super(InvariantReturnValueException, self).__init__(
            'Invariants must return a boolean value'
        )
