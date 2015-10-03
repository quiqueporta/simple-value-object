from inspect import getargspec
import inspect

from .exceptions import NotDeclaredArgsException, ArgWithoutValueException,\
    CannotBeChangeException, ViolatedInvariantException,\
    InvariantReturnValueException

MIN_NUMBER_ARGS = 1


class ValueObject(object):

    def __new__(cls, *args, **kwargs):
        self = super(ValueObject, cls).__new__(cls)

        args_spec = ArgsSpec(self.__init__)

        def check_class_are_initialized():
            no_arguments_in_init_constructor = len(args_spec.args) <= MIN_NUMBER_ARGS
            if no_arguments_in_init_constructor:
                raise NotDeclaredArgsException()
            if None in args:
                raise ArgWithoutValueException()

        def assign_instance_arguments():
            assign_default_values(args_spec)
            override_default_values_with_args(args_spec)

        def assign_default_values(args_spec):
            defaults = () if not args_spec.defaults else args_spec.defaults
            self.__dict__.update(
                dict(zip(args_spec.args[:0:-1], defaults[::-1]))
            )

        def override_default_values_with_args(args_spec):
            self.__dict__.update(
                dict(list(zip(args_spec.args[1:], args)) + list(kwargs.items()))
            )

        def check_invariants():
            # if not isinstance(self.invariants, tuple):
            #     raise InvariantsNotTupleException()

            for invariant in obtain_invariants():
                if not invariant_execute(invariant):
                    raise ViolatedInvariantException(
                        'Args values {} violates invariant: {}'.format(
                            list(self.__dict__.values()), invariant
                        )
                    )

        def invariant_execute(invariant):
            try:
                return_value = getattr(self, invariant)(self)
            except AttributeError:
                raise NotImplementedInvariant(
                    'Invariant {} needs to be implemented'.format(invariant)
                )

            if not isinstance(return_value, bool):
                raise InvariantReturnValueException()

            return return_value

        def obtain_invariants():
            for member in inspect.getmembers(cls):
                try:
                    is_method = hasattr(member[1], '__call__')
                    is_a_invariant_method = 'invariant_func_wrapper' in inspect.getsourcelines(member[1].__code__)[0][0]
                    if is_method and is_a_invariant_method:
                        yield(member[0])
                except AttributeError:
                    continue

        check_class_are_initialized()
        assign_instance_arguments()
        check_invariants()

        return self

    def __setattr__(self, name, value):
        raise CannotBeChangeException()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return self.__dict__ != other.__dict__

    @property
    def hash(self):
        return hash(self.__class__) and hash(frozenset(self.__dict__.items()))


class ArgsSpec(object):

    def __init__(self, method):
        try:
            self._args, self._varargs, self._keywords, self._defaults = getargspec(method)
        except TypeError:
            raise NotDeclaredArgsException()

    @property
    def args(self):
        return self._args

    @property
    def varargs(self):
        return self._varargs

    @property
    def keywords(self):
        return self._keywords

    @property
    def defaults(self):
        return self._defaults
