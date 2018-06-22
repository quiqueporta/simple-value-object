Value Object
============

|Version Number| |Build Status| |Coverage Status| |Requirements Status| |Python Version| |License GPLv3|


Based on Ruby Gem by NoFlopSquad (https://github.com/noflopsquad/value-object)


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
    # CannotBeChangeException: You cannot change values from a Value Object, create a new one

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
    # CannotBeChangeException: You cannot change values from a Value Object, create a new one


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

.. code-block:: python

    from simple_value_object import ValueObject, invariant

    class Point(ValueObject):

        def __init__(self, x, y):
            pass

        @invariant
        def inside_first_quadrant(cls, instance):
            return instance.x > 0 and instance.y > 0

        @invariant
        def x_less_than_y(cls, instance):
            return instance.x < instance.y

    Point(-5, 3)
    #ViolatedInvariantException: Args values [-5, 3] violates invariant: inside_first_cuadrant

    Point(6, 3)
    #ViolatedInvariantException: Args values [6, 3] violates invariant: x_less_than_y

    Point(1,3)
    #<__main__.Point at 0x7f2bd043c780>


Mutable types not allowed
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from simple_value_object import ValueObject, invariant

    class AValueObject(ValueObject):

        def __init__(self, an_arg):
            pass

    AValueObject(an_arg={'key': 'value'})
    #MutableTypeNotAllowedException: 'an_arg' cannot be a mutable data type.

    AValueObject({'key': 'value'})
    #MutableTypeNotAllowedException: Mutable args are not allowed.


Test
----

.. code-block:: sh

    > pip install -r requirements-test.txt
    > PYTHONPATH=$PYTHONPATH:. mamba


.. |Version Number| image:: https://img.shields.io/badge/version-1.0.0-blue.svg

.. |Build Status| image:: https://travis-ci.org/quiqueporta/simple-value-object.svg?branch=master
    :target: https://travis-ci.org/quiqueporta/simple-value-object

.. |Coverage Status| image:: https://coveralls.io/repos/quiqueporta/simple-value-object/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/quiqueporta/simple-value-object?branch=master

.. |Requirements Status| image:: https://requires.io/github/quiqueporta/simple-value-object/requirements.svg?branch=master
     :target: https://requires.io/github/quiqueporta/simple-value-object/requirements/?branch=master
          :alt: Requirements Status

.. |License GPLv3| image:: https://img.shields.io/badge/license-GPLv3-red.svg
    :target: https://opensource.org/licenses/GPL-3.0

.. |Python Version| image:: https://img.shields.io/badge/python-2.7,_3.3,_3.4,_3.5-blue.svg
