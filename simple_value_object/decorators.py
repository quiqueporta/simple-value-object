def invariant(func):
    def invariant_func_wrapper(cls, instance):
        return func(cls, instance)

    return invariant_func_wrapper


def param_invariant(func):
    def param_invariant_func_wrapper(cls, instance):
        return func(cls, instance)

    return param_invariant_func_wrapper
