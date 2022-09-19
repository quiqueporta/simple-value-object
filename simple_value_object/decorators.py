def invariant(func):
    def invariant_func_wrapper(instance):
        return func(instance)

    invariant_func_wrapper.name = func.__name__
    return invariant_func_wrapper
