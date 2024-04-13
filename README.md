# Value Object

![Version number](https://img.shields.io/badge/version-3.0.0-blue.svg) ![License MIT](https://img.shields.io/github/license/quiqueporta/simple-value-object) ![Python Version](https://img.shields.io/badge/python-3.7,_3.8,_3.9,_3.10,3.11,3.12-blue.svg)

Based on Ruby Gem by [NoFlopSquad](https://github.com/noflopsquad/value-object)

A **value object** is a small object that represents a simple entity whose equality isn't based on identity:
i.e. two value objects are equal when they have the same value, not necessarily being the same object.

[Wikipedia](http://en.wikipedia.org/wiki/Value_object)

## New version 3.0

This new version is a complete rewrite of the library, now it uses data classes to define the value objects.
With this change we can use type hints to define the fields and the library will take care of the rest.
Now you have autocomplete and type checking in your IDE. With the previous version, you did no autocomplete or type-checking.
You should be able to use this library with any version of Python 3.7 or higher.

## Installation

```sh
pip install simple-value-object
```

## Usage

### Constructor and field readers

```python
from simple_value_object import ValueObject

class Point(ValueObject):
    x: int
    y: int

point = Point(1, 2)

point.x
# 1

point.y
# 2

point.x = 5
# CannotBeChanged: You cannot change values from a Value Object, create a new one

class Date(ValueObject):
    day: int
    month: int
    year: int

date = Date(1, 10, 2015)

date.day
# 1

date.month
# 10

date.year
# 2015

date.month = 5
# CannotBeChanged: You cannot change values from a Value Object, create a new one
```

### Equality based on field values

```python
from simple_value_object import ValueObject

class Point(ValueObject):
    x: int
    y: int


a_point = Point(5, 3)

same_point = Point(5, 3)

a_point == same_point
# True

a_different_point = Point(6, 3)

a_point == a_different_point
# False
```

### Hash code based on field values

```python
from simple_value_object import ValueObject

class Point(ValueObject):
    x: int
    y: int

a_point = Point(5, 3)

same_point = Point(5, 3)

a_point.hash == same_point.hash
# True

a_different_point = Point.new(6, 3)

a_point.hash == a_different_point.hash
# False
```

### Invariants

Invariants **must** return a boolean value.

```python
from simple_value_object import ValueObject, invariant

class Point(ValueObject):
    x: int
    y: int

    @invariant
    def inside_first_quadrant(self):
        return self.x > 0 and self.y > 0

    @invariant
    def x_lower_than_y(self):
        return self.x < self.y

Point(-5, 3)
#InvariantViolation: inside_first_cuadrant

Point(6, 3)
#InvariantViolation: x_lower_than_y

Point(1,3)
#<__main__.Point at 0x7f2bd043c780>
```

### ValueObject within ValueObject

```python
from simple_value_object import ValueObject, invariant

class Currency(ValueObject):
    symbol: str

class Money(ValueObject):
    amount: Decimal
    currency: Currency

Money(amount=Decimal("100"), currency=Currency(symbol="€"))
```

## Tests

```sh
docker/test
```
