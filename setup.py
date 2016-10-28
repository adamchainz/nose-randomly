#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(filename):
    """
    Return package version as listed in `__version__` in `filename`.
    """
    init_py = open(filename).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('nose_randomly.py')

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

setup(
    name='nose-randomly',
    version=version,
    description="Nose plugin to randomly order tests and control random.seed.",
    long_description=readme + '\n\n' + history,
    author="Adam Johnson",
    author_email='me@adamj.eu',
    url='https://github.com/adamchainz/nose-randomly',
    py_modules=['nose_randomly'],
    include_package_data=True,
    install_requires=[
        'nose',
    ],
    license="BSD",
    zip_safe=False,
    keywords='nose, random, randomize, randomise, randomly',
    entry_points={
        'nose.plugins.0.10': ['randomly = nose_randomly:RandomlyPlugin'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
