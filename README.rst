Value Object
============

|Version Number| |Python Version| |License MIT|


Based on Ruby Gem by NoFlopSquad (https://github.com/noflopsquad/value-object)

A **value object** is a small object that represents a simple entity whose equality isn't based on identity:
i.e. two value objects are equal when they have the same value, not necessarily being the same object.


`Wikipedia <http://en.wikipedia.org/wiki/Value_object/>`_.


Installation
------------

.. code-block:: sh

    > pip install simple-value-object

Usage
-----

Constructor and field readers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from simple_value_object import ValueObject

    class Point(ValueObject):
        def __init__(self, x, y):
            pass

    point = Point(1, 2)

    point.x
    # 1

    point.y
    # 2

    point.x = 5
    # CannotBeChanged: You cannot change values from a Value Object, create a new one

    class Date(ValueObject):
        def __init__(self, day, month, year):
            pass

    date = Date(1, 10, 2015)

    date.day
    # 1

    date.month
    # 10

    date.year
    # 2015

    date.month = 5
    # CannotBeChanged: You cannot change values from a Value Object, create a new one


Equality based on field values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from simple_value_object import ValueObject

    class Point(ValueObject):
        def __init__(self, x, y):
            pass

    a_point = Point(5, 3)

    same_point = Point(5, 3)

    a_point == same_point
    # True

    a_different_point = Point(6, 3)

    a_point == a_different_point
    # False


Hash code based on field values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from simple_value_object import ValueObject

    class Point(ValueObject):
        def __init__(self, x, y):
            pass

    a_point = Point(5, 3)

    same_point = Point(5, 3)

    a_point.hash == same_point.hash
    # True

    a_different_point = Point.new(6, 3)

    a_point.hash == a_different_point.hash
    # False


Invariants
~~~~~~~~~~

Invariants **must** return a boolean value.

.. code-block:: python

    from simple_value_object import ValueObject, invariant

    class Point(ValueObject):

        def __init__(self, x, y):
            pass

        @invariant
        def inside_first_quadrant(self):
            return self.x > 0 and self.y > 0

        @invariant
        def x_less_than_y(self):
            return self.x < self.y

    Point(-5, 3)
    #InvariantViolation: inside_first_cuadrant

    Point(6, 3)
    #InvariantViolation: x_less_than_y

    Point(1,3)
    #<__main__.Point at 0x7f2bd043c780>


ValueObject within ValueObject
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from simple_value_object import ValueObject, invariant

    class Money(ValueObject):
        def __init__(self, amount, currency):
            pass

    class Currency(ValueObject):
        def __init__(self, symbol):
            pass

    Money(amount=100, currency=Currency(symbol="€"))


Test
----

.. code-block:: sh

    > $ docker/test


.. |Version Number| image:: https://img.shields.io/badge/version-2.0.0-blue.svg

.. |License MIT| image:: https://img.shields.io/github/license/quiqueporta/simple-value-object

.. |Python Version| image:: https://img.shields.io/badge/python-3.6,_3.7,_3.8,_3.9,_3.10-blue.svg
