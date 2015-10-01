class NotDeclaredArgsException(Exception):
    pass


class ArgWithoutValueException(Exception):
    pass


class CannotBeChangeException(Exception):
    pass


class ViolatedInvariantException(Exception):
    pass


class NotImplementedInvariant(Exception):
    pass


class InvariantsNotTupleException(Exception):
    def __init__(self, *args, **kwargs):
        super(InvariantsNotTupleException, self).__init__('Invariants is not a valid tuple.')


class InvariantReturnValueException(Exception):
    def __init__(self, *args, **kwargs):
        super(InvariantReturnValueException, self).__init__('Invariants must return a boolean value')
