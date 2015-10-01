from setuptools import setup

from simple_value_object import get_version


setup(
    name='simple-value-object',
    version=get_version(),
    license='GPLv3',
    author='Quique Porta',
    author_email='quiqueporta@gmail.com',
    description='A simple mixin for create Value Objects',
    long_description=open('README.rst').read(),
    url='https://github.com/quiqueporta/value-object',
    download_url='https://github.com/quiqueporta/simple-value-object/releases',
    keywords=['python', 'ddd'],
    packages=['simple_value_object'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
    ],
)
