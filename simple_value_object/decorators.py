import functools
from .exceptions import InvariantMustReturnBool, InvariantViolation


def invariant(func=None, *, exception_type=None):
    # Decorator called with parentheses and arguments
    if func is None:
        return lambda f: invariant(f, exception_type=exception_type)

    # Decorator called without parentheses or with parentheses but without arguments
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        message = ""

        if isinstance(result, tuple):
            result, message = result[0], result[1]

        if not isinstance(result, bool):
            raise InvariantMustReturnBool()

        if result is False:
            if exception_type:
                raise exception_type(message)
            raise InvariantViolation(f"Invariant violation: {func.__name__}")

        return result

    setattr(wrapper, "_invariant", True)

    return wrapper
