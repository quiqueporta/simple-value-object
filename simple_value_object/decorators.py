def invariant(func):
    def invariant_func_wrapper(instance):
        return func(instance)

    invariant_func_wrapper.name = func.__name__
    setattr(invariant_func_wrapper, "_invariant", True)

    return invariant_func_wrapper
