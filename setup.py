#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'pypi':
    os.system('python setup.py sdist bdist_wheel upload')
    sys.exit()

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='OBB_Maya',
    version='0.1.0',
    description="Oriented Bounding Boxes in Maya.",
    long_description=readme,
    author="Christopher DeVito",
    author_email='chrisdevito@chribis.com',
    url='https://github.com/chrisdevito/OBB',
    packages=[
        'OBB',
    ],
    package_dir={'OBB':
                 'OBB'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='OBB',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
