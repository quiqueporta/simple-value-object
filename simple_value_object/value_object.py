import hashlib
from dataclasses import dataclass, FrozenInstanceError


class ValueObject:
    def __init_subclass__(cls):
        cls = dataclass(cls, frozen=True)

    def __post_init__(self):
        self.__replace_mutable_fields_with_immutable()
        self.__check_invariants()

    @property
    def hash(self):
        return int(self.__calculate_hash(), 16)

    def __replace_mutable_fields_with_immutable(self):
        mutable_types = {
            dict: immutable_dict,
            list: immutable_list,
            set: immutable_set,
        }
        for field in self.__get_mutable_fields():
            object.__setattr__(
                self,
                field.name,
                mutable_types[field.type](getattr(self, field.name)),
            )

    def __get_mutable_fields(self):
        return filter(
            lambda field: field.type in (dict, list, set),
            self.__dataclass_fields__.values(),
        )

    def __check_invariants(self):
        for invariant in self.__obtain_invariants():
            invariant()

    def __obtain_invariants(self):
        invariant_methods = [
            method
            for method in dir(self)
            if callable(getattr(self, method))
            and hasattr(getattr(self, method), "_invariant")
        ]
        for invariant in invariant_methods:
            yield getattr(self, invariant)

    def __calculate_hash(self):
        hash_content = "".join(str(value) for value in self.__dict__.values())
        return hashlib.sha256(hash_content.encode()).hexdigest()

    def __hash__(self):
        return self.hash

    def __str__(self):
        return repr(self)

    def __repr__(self):
        class_name = self.__class__.__name__.split(".")[-1]
        attribute_str = ", ".join(
            f"{key}={value}" for key, value in self.__dict__.items()
        )
        return f"{class_name}({attribute_str})"


class immutable_dict(dict):

    def _immutable(self, *args, **kwargs):
        raise FrozenInstanceError()

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear = _immutable
    update = _immutable
    setdefault = _immutable
    pop = _immutable
    popitem = _immutable


class immutable_list(list):

    def _immutable(self, *args, **kwargs):
        raise FrozenInstanceError()

    __setitem__ = _immutable
    __delitem__ = _immutable
    append = _immutable
    extend = _immutable
    insert = _immutable
    pop = _immutable
    remove = _immutable
    clear = _immutable
    reverse = _immutable
    sort = _immutable


class immutable_set(set):

    def _immutable(self, *args, **kwargs):
        raise FrozenInstanceError()

    add = _immutable
    clear = _immutable
    difference_update = _immutable
    discard = _immutable
    intersection_update = _immutable
    pop = _immutable
    remove = _immutable
    symmetric_difference_update = _immutable
    update = _immutable
