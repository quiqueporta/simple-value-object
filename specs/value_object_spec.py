from expects import *

from value_object import ValueObject
from value_object.exceptions import NotDeclaredArgsException, ArgWithoutValueException, CannotBeChangeException, \
    ViolatedInvariantException, NotImplementedInvariant, InvariantsNotTupleException, InvariantReturnValueException


class Point(ValueObject):
    def __init__(self, x, y):
        pass

with description('Value Object'):
    with context('standard behavior'):
        with it('generates constructor, fields and accessors for declared fields'):
            a_value_object = Point(5, 3)
            expect(a_value_object.x).to(equal(5))
            expect(a_value_object.y).to(equal(3))

        with it('provides equality based on declared fields values'):
            a_value_object = Point(5, 3)
            same_value_object = Point(5, 3)
            different_value_object = Point(6, 3)

            expect(a_value_object).to(equal(same_value_object))
            expect(a_value_object).not_to(equal(different_value_object))
            expect(a_value_object != different_value_object).to(be(True))

        with it('provides hash code generation based on declared fields values'):
            a_value_object = Point(5, 3)
            same_value_object = Point(5, 3)
            different_value_object = Point(6, 3)
            expect(a_value_object.hash).to(equal(same_value_object.hash))
            expect(a_value_object.hash).not_to(equal(different_value_object.hash))

        with it('values can not be changed'):
            a_value_object = Point(5, 3)
            expect(lambda: setattr(a_value_object, 'x', 4)).to(
                raise_error(CannotBeChangeException, 'You cannot change values from a Value Object, create a new one')
            )

        with it('can set default values'):
            class MyPoint(ValueObject):
                def __init__(self, x, y=3):
                    pass
            a_value_object = MyPoint(5)
            expect(a_value_object.y).to(equal(3))

    with context('restrictions'):
        with context('on initialization'):
            with it ('must at least have one arg in __init__'):
                class DummyWithNoArgsInInit(ValueObject):
                    pass
                expect(lambda: DummyWithNoArgsInInit()).to(
                    raise_error(NotDeclaredArgsException, 'No arguments declared in __init__')
                )
            with it ('must not have any arg initialized to None'):
                class DummyWithDeclaredFieldsWithoutValue(ValueObject):
                    def __init__(self, x, y):
                        pass
                expect(lambda: DummyWithDeclaredFieldsWithoutValue(1, None)).to(raise_error(ArgWithoutValueException))
            with it('must have number of values equal to number of args'):
                expect(lambda: Point(1)).to(raise_error(TypeError))
                expect(lambda: Point(1, 2, 3)).to(raise_error(TypeError))

    with context('forcing invariants'):
        with it('forces declared invariants'):
            class AnotherPoint(ValueObject):

                invariants = ('inside_first_quadrant', 'x_less_than_y')

                def __init__(self, x, y):
                    pass

                @classmethod
                def inside_first_quadrant(cls, instance):
                    return instance.x > 0 and instance.y > 0

                @classmethod
                def x_less_than_y(cls, instance):
                    return instance.x < instance.y

            expect(lambda: AnotherPoint(-5, 3)).to(
                raise_error(ViolatedInvariantException)
            )

            expect(lambda: AnotherPoint(6, 3)).to(
                raise_error(ViolatedInvariantException)
            )

        with it('raises an exception when a declared invariant is not a valid tuple'):
            class PairOfFloats(ValueObject):
                invariants = ('floats')

                def __init__(self, x, y):
                    pass

            expect(lambda: PairOfFloats(5, 2)).to(raise_error(InvariantsNotTupleException))

        with it('raises an exception when a declared invariant has not been implemented'):
            class PairOfIntegers(ValueObject):
                invariants = ('integers',)

                def __init__(self, x, y):
                    pass

            expect(lambda: PairOfIntegers(5, 2)).to(raise_error(NotImplementedInvariant,
                                                                'Invariant integers needs to be implemented'))

        with it('raises an exception when a declared invariant doesnt returns a boolean value'):
            class Date(ValueObject):
                invariants = ('first_year_quarter',)

                def __init__(self, day, month, year):
                    pass

                @classmethod
                def first_year_quarter(cls, instance):
                    return 0

            expect(lambda: Date(8, 6, 2002)).to(raise_error(InvariantReturnValueException))
