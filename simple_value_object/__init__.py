# -*- coding: utf-8 -*-

from .value_object import ValueObject
from .decorators import invariant

VERSION = (0, 2, 1, 'final')
__version__ = VERSION


def get_version():
    version = '{}.{}'.format(VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '{}.{}'.format(version, VERSION[2])
    if VERSION[3:] == ('alpha', 0):
        version = '{} pre-alpha'.format(version)
    else:
        if VERSION[3] != 'final':
            version = '{} {}'.format(version, VERSION[3])
    return version
