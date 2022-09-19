import inspect
import sys

from .exceptions import (
    CannotBeChanged,
    ConstructorWithoutArguments,
    InvariantMustReturnBool,
    InvariantViolation
)

MIN_NUMBER_ARGS = 1
INVARIANT_NAME = 0
INVARIANT_METHOD = 1


class ValueObject:

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)

        args_spec = ArgsSpec(self.__init__)

        def check_class_initialization():
            init_constructor_without_arguments = len(args_spec.args) <= MIN_NUMBER_ARGS

            if init_constructor_without_arguments:
                raise ConstructorWithoutArguments()

        def replace_mutable_kwargs_with_immutable_types():
            for arg, value in kwargs.items():
                if isinstance(value, dict):
                    kwargs[arg] = immutable_dict(value)
                if isinstance(value, list):
                    kwargs[arg] = tuple(value)
                if isinstance(value, set):
                    kwargs[arg] = frozenset(value)

        def assign_instance_arguments():
            assign_default_values()
            override_default_values_with_args()

        def assign_default_values():
            defaults = () if not args_spec.defaults else args_spec.defaults
            self.__dict__.update(
                dict(zip(args_spec.args[:0:-1], defaults[::-1]))
            )

        def override_default_values_with_args():
            sanitized_args = []
            for arg in args:
                if isinstance(arg, dict):
                    sanitized_args.append(immutable_dict(arg))
                elif isinstance(arg, (list, set)):
                    sanitized_args.append(tuple(arg))
                else:
                    sanitized_args.append(arg)

            self.__dict__.update(
                dict(list(zip(args_spec.args[1:], sanitized_args)) + list(kwargs.items()))
            )

        def check_invariants():
            for invariant in obtain_invariants():
                if is_invariant_violated(invariant):
                    raise InvariantViolation(f'Invariant violation: {invariant.name}')

        def obtain_invariants():
            for invariant in filter(is_invariant, cls.__dict__.values()):
                yield invariant

        def is_invariant(method):
            return hasattr(method, '__call__') and method.__name__ == 'invariant_func_wrapper'

        def is_invariant_violated(invariant):
            invariant_result = invariant(self)

            if not isinstance(invariant_result, bool):
                raise InvariantMustReturnBool()

            return invariant_result is False


        check_class_initialization()
        replace_mutable_kwargs_with_immutable_types()
        assign_instance_arguments()
        check_invariants()

        return self

    def __setattr__(self, name, value):
        raise CannotBeChanged()

    def __eq__(self, other):
        if other is None:
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return self.__dict__ != other.__dict__

    def __str__(self):
        return repr(self)

    def __repr__(self):
        args_spec = ArgsSpec(self.__init__)
        args_values = ["{}={}".format(arg, getattr(self, arg)) for arg in args_spec.args[1:]]

        return "{}({})".format(self.__class__.__name__, ", ".join(args_values))

    def __hash__(self):
        return self.hash

    @property
    def hash(self):
        return hash(repr(self))


class ArgsSpec:

    def __init__(self, method):
        self.__argspec = inspect.getfullargspec(method)
        self.__varkw = self.__argspec.varkw

    @property
    def args(self):
        return self.__argspec.args

    @property
    def varargs(self):
        return self.__argspec.varargs

    @property
    def keywords(self):
        return self.__varkw

    @property
    def defaults(self):
        return self.__argspec.defaults


class immutable_dict(dict):

    def __hash__(self):
        return id(self)

    def _immutable(self, *args, **kwargs):
        raise CannotBeChanged()

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear = _immutable
    update = _immutable
    setdefault = _immutable
    pop = _immutable
    popitem = _immutable
