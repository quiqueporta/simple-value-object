def invariant(func):
    def invariant_func_wrapper(cls, instance):
        return func(cls, instance)

    return invariant_func_wrapper
