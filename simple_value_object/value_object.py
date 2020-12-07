import sys
import inspect

from .exceptions import (
    CannotBeChangeException,
    InvariantReturnValueException,
    NotDeclaredArgsException,
    ViolatedInvariantException
)

MIN_NUMBER_ARGS = 1
INVARIANT_NAME = 0
INVARIANT_METHOD = 1


class ValueObject(object):

    def __new__(cls, *args, **kwargs):
        self = super(ValueObject, cls).__new__(cls)

        args_spec = ArgsSpec(self.__init__)

        def check_class_initialization():
            init_constructor_without_arguments = len(args_spec.args) <= MIN_NUMBER_ARGS

            if init_constructor_without_arguments:
                raise NotDeclaredArgsException()

        def replace_mutable_kwargs_with_immutable_types():
            for arg, value in kwargs.items():
                if isinstance(value, dict):
                    kwargs[arg] = immutable_dict(value)
                if isinstance(value, (list, set)):
                    kwargs[arg] = tuple(value)

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
                if not invariant_execute(invariant[INVARIANT_METHOD]):
                    raise ViolatedInvariantException(
                        'Args violates invariant: {}'.format(
                            invariant[INVARIANT_NAME]
                        )
                    )

        def invariant_execute(invariant):
            return_value = invariant(self, self)

            if not isinstance(return_value, bool):
                raise InvariantReturnValueException()

            return return_value

        def is_invariant(method):
            try:
                return 'invariant_func_wrapper' in str(method) and '__init__' not in str(method)
            except TypeError:
                return False

        def obtain_invariants():
            invariants = [(member[INVARIANT_NAME], member[INVARIANT_METHOD]) for member in inspect.getmembers(cls, is_invariant)]
            for invariant in invariants:
                yield invariant

        check_class_initialization()
        replace_mutable_kwargs_with_immutable_types()
        assign_instance_arguments()
        check_invariants()

        return self

    def __setattr__(self, name, value):
        raise CannotBeChangeException()

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


class ArgsSpec(object):

    def __init__(self, method):
        try:
            if sys.version_info.major == 2:
                self.__argspec = inspect.getargspec(method)
                self.__varkw = self.__argspec.keywords
            else:
                self.__argspec = inspect.getfullargspec(method)
                self.__varkw = self.__argspec.varkw
        except TypeError:
            raise NotDeclaredArgsException()

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
        raise CannotBeChangeException()

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear = _immutable
    update = _immutable
    setdefault = _immutable
    pop = _immutable
    popitem = _immutable
