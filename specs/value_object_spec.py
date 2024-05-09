from expects import *
from decimal import Decimal
from mamba import context, description, it

from simple_value_object import ValueObject, invariant

from simple_value_object.exceptions import (
    CannotBeChanged,
    InvariantViolation,
    InvariantMustReturnBool,
)


class Point(ValueObject):
    x: int
    y: int


class PointWithDefault(ValueObject):
    x: int
    y: int = 3


class Currency(ValueObject):
    symbol: str


class Money(ValueObject):
    amount: Decimal
    currency: Currency


class ValueObjectWithDict(ValueObject):
    a_dict: dict


class ValueObjectWithList(ValueObject):
    a_list: list


class ValueObjectWithSet(ValueObject):
    a_set: set


class PointWithInvariants(ValueObject):
    x: int
    y: int

    @invariant
    def inside_first_quadrant(self):
        return self.x > 0 and self.y > 0

    @invariant
    def x_lower_than_y(self):
        return self.x < self.y


with description("Value Object"):

    with context("standard behavior"):

        with it("generates constructor, fields and accessors for declared fields"):
            a_point = Point(5, 3)

            expect(a_point.x).to(equal(5))
            expect(a_point.y).to(equal(3))

        with it("provides equality based on declared fields values"):
            a_point = Point(5, 3)
            same_point = Point(5, 3)
            different_point = Point(6, 3)

            expect(a_point).to(equal(same_point))
            expect(a_point).not_to(equal(different_point))
            expect(a_point != different_point).to(be_true)

        with it("provides hash code generation based on declared fields values"):
            a_point = Point(5, 3)
            same_point = Point(5, 3)
            different_point = Point(6, 3)

            expect(a_point.hash).to(equal(same_point.hash))
            expect(a_point.hash).not_to(equal(different_point.hash))

        with it("values can not be changed"):
            a_point = Point(5, 3)

            def change_point():
                a_point.x = 4

            expect(lambda: change_point()).to(
                raise_error(
                    CannotBeChanged,
                    "You cannot change values from a Value Object, create a new one",
                )
            )

        with it("can set default values"):

            class MyPoint(ValueObject):
                x: int
                y: int = 3

            my_point = MyPoint(5)
            expect(my_point.x).to(equal(5))
            expect(my_point.y).to(equal(3))

        with it("can set another value object as parameter"):
            a_money = Money(Decimal("100"), Currency("€"))

            expect(a_money).to(equal(Money(Decimal("100"), Currency("€"))))
            expect(a_money.currency).to(equal(Currency("€")))

        with it("can compare hash for value objects within value objects"):
            a_money = Money(Decimal("100"), Currency("€"))

            another_money = Money(Decimal("100"), Currency("€"))
            expect(a_money.hash).to(equal(another_money.hash))

        with it("provides a representation"):

            a_point_object = Point(6, 7)
            a_point_object_with_defaults = PointWithDefault(6)
            a_point_object_within_value_object = Money(Decimal("100"), Currency("€"))

            expect(str(a_point_object)).to(equal("Point(x=6, y=7)"))
            expect(repr(a_point_object)).to(equal("Point(x=6, y=7)"))
            expect(str(a_point_object_with_defaults)).to(
                equal("PointWithDefault(x=6, y=3)")
            )
            expect(repr(a_point_object_with_defaults)).to(
                equal("PointWithDefault(x=6, y=3)")
            )
            expect(str(a_point_object_within_value_object)).to(
                equal("Money(amount=Decimal('100'), currency=Currency(symbol='€'))")
            )
            expect(repr(a_point_object_within_value_object)).to(
                equal("Money(amount=Decimal('100'), currency=Currency(symbol='€'))")
            )

    with context("restrictions"):

        with context("with mutable data types"):

            with it("does not allow to change dicts arguments"):

                a_value_object = ValueObjectWithDict(a_dict={"key": "value"})
                another_value_object = ValueObjectWithDict({"key": "value"})

                expect(
                    lambda: a_value_object.a_dict.update({"key": "another_value"})
                ).to(raise_error(CannotBeChanged))
                expect(
                    lambda: another_value_object.a_dict.update({"key": "another_value"})
                ).to(raise_error(CannotBeChanged))
                expect(lambda: a_value_object.a_dict.clear()).to(
                    raise_error(CannotBeChanged)
                )
                expect(lambda: another_value_object.a_dict.clear()).to(
                    raise_error(CannotBeChanged)
                )

                def remove_key():
                    del a_value_object.a_dict["key"]
                    del another_value_object.a_dict["key"]

                expect(lambda: remove_key()).to(raise_error(CannotBeChanged))

                def change_key():
                    a_value_object.a_dict["key"] = "new_value"
                    another_value_object.a_dict["key"] = "new_value"

                expect(lambda: change_key()).to(raise_error(CannotBeChanged))
                expect(lambda: a_value_object.a_dict.pop()).to(
                    raise_error(CannotBeChanged)
                )
                expect(lambda: another_value_object.a_dict.pop()).to(
                    raise_error(CannotBeChanged)
                )
                expect(lambda: a_value_object.a_dict.popitem()).to(
                    raise_error(CannotBeChanged)
                )
                expect(lambda: another_value_object.a_dict.popitem()).to(
                    raise_error(CannotBeChanged)
                )
                expect(lambda: a_value_object.a_dict.setdefault("key")).to(
                    raise_error(CannotBeChanged)
                )
                expect(lambda: another_value_object.a_dict.setdefault("key")).to(
                    raise_error(CannotBeChanged)
                )

            with it("does not allow to change lists arguments"):

                a_value_object = ValueObjectWithList(a_list=[1, 2, 3])
                another_value_object = ValueObjectWithList([1, 2, 3])

                def change_list_item():
                    a_value_object.a_list[0] = 4
                    another_value_object.a_list[0] = 4

                expect(lambda: change_list_item()).to(raise_error(CannotBeChanged))

                def delete_list_item():
                    del a_value_object.a_list[0]
                    del another_value_object.a_list[0]

                expect(lambda: delete_list_item()).to(raise_error(CannotBeChanged))
                expect(lambda: a_value_object.a_list.clear()).to(
                    raise_error(CannotBeChanged)
                )
                expect(lambda: another_value_object.a_list.clear()).to(
                    raise_error(CannotBeChanged)
                )

            with it("does not allow to change set arguments"):

                a_value_object = ValueObjectWithSet(a_set=set([1, 2, 3]))
                another_value_object = ValueObjectWithSet(set([1, 2, 3]))

                def change_list_item():
                    a_value_object.a_set.clear()
                    another_value_object.a_set.clear()

                expect(lambda: change_list_item()).to(raise_error(CannotBeChanged))

    with context("forcing invariants"):

        with it("forces declared invariants"):

            expect(lambda: PointWithInvariants(5, -3)).to(
                raise_error(
                    InvariantViolation, "Invariant violation: inside_first_quadrant"
                )
            )

            expect(lambda: PointWithInvariants(6, 3)).to(
                raise_error(InvariantViolation, "Invariant violation: x_lower_than_y")
            )

        with it(
            "raises an exception when a declared invariant doesnt returns a boolean value"
        ):

            class Date(ValueObject):
                day: int
                month: int
                year: int

                @invariant
                def first_year_quarter(self):
                    return 0

            expect(lambda: Date(8, 6, 2002)).to(raise_error(InvariantMustReturnBool))

    with context("ensures that defined data types are respected"):

        with it("raises an exception when a field is not the expected type"):
            expect(lambda: Point("5", 3)).to(
                raise_error(TypeError, "x must be of type <class 'int'>")
            )
            expect(lambda: Point(5, "3")).to(
                raise_error(TypeError, "y must be of type <class 'int'>")
            )
        with it(
            "raises an exception when a inner value object is not the expected type"
        ):
            expect(lambda: Money(Decimal("100"), "€")).to(
                raise_error(
                    TypeError,
                    "currency must be of type <class 'specs/value_object_spec.Currency'>",
                )
            )
