# -*- coding: utf-8 -*-
import codecs
import re

from setuptools import setup


def get_version(filename):
    with codecs.open(filename, 'r', 'utf-8') as fp:
        contents = fp.read()
    return re.search(r"__version__ = ['\"]([^'\"]+)['\"]", contents).group(1)


version = get_version('nose_randomly.py')

with codecs.open('README.rst', 'r', 'utf-8') as readme_file:
    readme = readme_file.read()

with codecs.open('HISTORY.rst', 'r', 'utf-8') as history_file:
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
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    license="BSD",
    zip_safe=False,
    keywords='nose, random, randomize, randomise, randomly',
    entry_points={
        'nose.plugins.0.10': ['randomly = nose_randomly:RandomlyPlugin'],
    },
    classifiers=[
        'Development Status :: 7 - Inactive',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
