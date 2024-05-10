# Changelog

## 3.0.1 (2024-05-10)

- Remove unused imports

## 3.0.0 (2024-04-13)

- Use python dataclass to create ValueObject

## 2.0.0 (2022-10-27)

- Rename CannotBeChangeException to CannotBeChanged
- Rename InvariantReturnValueException to InvariantMustReturnBool
- Rename NotDeclaredArgsException to ConstructorWithoutArguments
- Rename ViolatedInvariantException to InvariantViolation
- Simplifly invariants now receives `self` attribute only
- Fix replace_mutable_kwargs_with_immutable_types for `set` kwargs

## 1.5.0 (2020-12-07)

- Allow None as params. You can control it with invariants.

## 1.4.0 (2020-06-13)

- Removing deprecation warnings
- Change license to MIT/X11

## 1.3.0 (2019-04-29)

- Allow mutable data types but restricted for modifications.

## 1.2.0 (2019-01-15)

- Reduced the creation time

## 1.1.1 (2015-09-05)

- Fix hash for value objects within value objects.

## 1.1.0 (2018-09-04)

- Fix value objects within value objects.
- Add value objects representation.

## 1.0.1 (2018-06-22)

- Mutable types are not allowed.

## 0.2.1 (2015-10-05)

- Removed unnecessary code.

## 0.2.0 (2015-10-03)

- Created a invariant decorator.

## 0.1.0 (2015-10-01)

- Initial release.
