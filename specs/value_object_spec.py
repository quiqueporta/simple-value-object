from expects import *
from mamba import (
    context,
    description,
    it
)
from simple_value_object import (
    ValueObject,
    invariant
)
from simple_value_object.exceptions import (
    ArgWithoutValueException,
    CannotBeChangeException,
    InvariantReturnValueException,
    NotDeclaredArgsException,
    ViolatedInvariantException
)


class Point(ValueObject):
    def __init__(self, x, y):
        pass


class Money(ValueObject):
    def __init__(self, amount, currency):
        pass


class Currency(ValueObject):
    def __init__(self, symbol):
        pass


with description('Value Object'):

    with context('standard behavior'):

        with it('generates constructor, fields and accessors for declared fields'):
            a_point = Point(5, 3)

            expect(a_point.x).to(equal(5))
            expect(a_point.y).to(equal(3))

        with it('provides equality based on declared fields values'):
            a_point = Point(5, 3)
            same_point = Point(5, 3)
            different_point = Point(6, 3)

            expect(a_point).to(equal(same_point))
            expect(a_point).not_to(equal(different_point))
            expect(a_point != different_point).to(be_true)

        with it('provides hash code generation based on declared fields values'):
            a_point = Point(5, 3)
            same_point = Point(5, 3)
            different_point = Point(6, 3)

            expect(a_point.hash).to(equal(same_point.hash))
            expect(a_point.hash).not_to(equal(different_point.hash))

        with it('values can not be changed'):
            a_point = Point(5, 3)

            def change_point():
                a_point.x = 4

            expect(lambda: change_point()).to(
                raise_error(CannotBeChangeException, 'You cannot change values from a Value Object, create a new one')
            )

        with it('can set default values'):
            class MyPoint(ValueObject):
                def __init__(self, x, y=3):
                    pass

            my_point = MyPoint(5)
            expect(my_point.x).to(equal(5))
            expect(my_point.y).to(equal(3))

        with it('can set another Value Object as parameter'):
            a_money = Money(100, Currency('€'))

            expect(a_money).to(equal(Money(100, Currency('€'))))
            expect(a_money.currency).to(equal(Currency('€')))

        with it('can compare hash for value objects within value objects'):
            a_money = Money(100, Currency('€'))

            another_money = Money(100, Currency('€'))
            expect(a_money.hash).to(equal(another_money.hash))

        with it('provides a representation'):
            class MyPoint(ValueObject):
                def __init__(self, x, y=3):
                    pass

            a_point_object = Point(6, 7)
            a_point_object_with_defaults = MyPoint(6)
            a_point_object_within_value_object = Money(100, Currency('€'))

            expect(str(a_point_object)).to(equal('Point(x=6, y=7)'))
            expect(repr(a_point_object)).to(equal('Point(x=6, y=7)'))
            expect(str(a_point_object_with_defaults)).to(equal('MyPoint(x=6, y=3)'))
            expect(repr(a_point_object_with_defaults)).to(equal('MyPoint(x=6, y=3)'))
            expect(str(a_point_object_within_value_object)).to(equal('Money(amount=100, currency=Currency(symbol=€))'))
            expect(repr(a_point_object_within_value_object)).to(equal('Money(amount=100, currency=Currency(symbol=€))'))

    with context('restrictions'):

        with context('on initialization'):

            with it ('must at least have one arg in __init__'):
                class WithNoArgs(ValueObject):
                    pass

                expect(lambda: WithNoArgs()).to(
                    raise_error(NotDeclaredArgsException, 'No arguments declared in __init__')
                )

            with it ('must not have any arg initialized to None'):
                expect(lambda: Point(1, None)).to(
                    raise_error(ArgWithoutValueException)
                )

            with it ('must not have any kwarg initialized to None'):
                expect(lambda: Point(1, y=None)).to(
                    raise_error(ArgWithoutValueException)
                )

            with it('must have number of values equal to number of args'):
                expect(lambda: Point(1)).to(raise_error(TypeError))
                expect(lambda: Point(1, 2, 3)).to(raise_error(TypeError))

        with context('with mutable data types'):

            with it('does not allow to change dicts arguments'):
                class AValueObject(ValueObject):
                    def __init__(self, a_dict):
                        pass
                a_value_object = AValueObject(a_dict={'key': 'value'})
                another_value_object = AValueObject({'key': 'value'})

                expect(lambda: a_value_object.a_dict.update({'key': 'another_value'})).to(
                    raise_error(CannotBeChangeException)
                )
                expect(lambda: another_value_object.a_dict.update({'key': 'another_value'})).to(
                    raise_error(CannotBeChangeException)
                )
                expect(lambda: a_value_object.a_dict.clear()).to(
                    raise_error(CannotBeChangeException)
                )
                expect(lambda: another_value_object.a_dict.clear()).to(
                    raise_error(CannotBeChangeException)
                )
                def remove_key():
                    del(a_value_object.a_dict['key'])
                    del(another_value_object.a_dict['key'])
                expect(lambda: remove_key()).to(
                    raise_error(CannotBeChangeException)
                )
                def change_key():
                    a_value_object.a_dict['key'] = 'new_value'
                    another_value_object.a_dict['key'] = 'new_value'
                expect(lambda: change_key()).to(
                    raise_error(CannotBeChangeException)
                )
                expect(lambda: a_value_object.a_dict.pop()).to(
                    raise_error(CannotBeChangeException)
                )
                expect(lambda: another_value_object.a_dict.pop()).to(
                    raise_error(CannotBeChangeException)
                )
                expect(lambda: a_value_object.a_dict.popitem()).to(
                    raise_error(CannotBeChangeException)
                )
                expect(lambda: another_value_object.a_dict.popitem()).to(
                    raise_error(CannotBeChangeException)
                )
                expect(lambda: a_value_object.a_dict.setdefault('key')).to(
                    raise_error(CannotBeChangeException)
                )
                expect(lambda: another_value_object.a_dict.setdefault('key')).to(
                    raise_error(CannotBeChangeException)
                )

            with it('does not allow to change lists arguments'):
                class AValueObject(ValueObject):
                    def __init__(self, a_list):
                        pass

                a_value_object = AValueObject(a_list=[1, 2, 3])
                another_value_object = AValueObject([1, 2, 3])

                def change_list_item():
                    a_value_object.a_list[0] = 4
                    another_value_object.a_list[0] = 4
                expect(lambda: change_list_item()).to(raise_error(TypeError))
                def delete_list_item():
                    del(a_value_object.a_list[0])
                    del(another_value_object.a_list[0])
                expect(lambda: delete_list_item()).to(raise_error(TypeError))
                expect(lambda: a_value_object.a_list.clear()).to(raise_error(AttributeError))
                expect(lambda: another_value_object.a_list.clear()).to(raise_error(AttributeError))

            with it('does not allow to change set arguments'):
                class AValueObject(ValueObject):
                    def __init__(self, a_set):
                        pass

                a_value_object = AValueObject(a_set=set([1, 2, 3]))
                another_value_object = AValueObject(set([1, 2, 3]))

                def change_list_item():
                    a_value_object.a_set.clear()
                    another_value_object.a_set.clear()

                expect(lambda: change_list_item()).to(raise_error(AttributeError))

    with context('forcing invariants'):

        with it('forces declared invariants'):
            class AnotherPoint(ValueObject):
                def __init__(self, x, y):
                    pass

                @invariant
                def inside_first_quadrant(cls, instance):
                    return instance.x > 0 and instance.y > 0

                @invariant
                def x_less_than_y(cls, instance):
                    return instance.x < instance.y

            expect(lambda: AnotherPoint(-5, 3)).to(
                raise_error(ViolatedInvariantException)
            )

            expect(lambda: AnotherPoint(6, 3)).to(
                raise_error(ViolatedInvariantException)
            )

        with it('raises an exception when a declared invariant doesnt returns a boolean value'):
            class Date(ValueObject):

                def __init__(self, day, month, year):
                    pass

                @invariant
                def first_year_quarter(cls, instance):
                    return 0

            expect(lambda: Date(8, 6, 2002)).to(raise_error(InvariantReturnValueException))
