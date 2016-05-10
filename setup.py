#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import platform
from setuptools import setup, find_packages

if sys.argv[-1] == 'pypi':
    os.system('python setup.py sdist bdist_wheel upload')
    sys.exit()

required_packages = ["numpy==1.9.2", "scipy==0.16.0"]

if platform.system() == "Windows":
    dependencies = ["https://pypi.anaconda.org/carlkl/simple numpy",
                    "https://pypi.anaconda.org/carlkl/scipy numpy"]

else:
    dependencies = []

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


setup(
    name='OBB_Maya',
    version='0.1.10',
    description="Oriented Bounding Boxes in Maya.",
    long_description=readme,
    install_requires=required_packages,
    author="Christopher DeVito",
    author_email='chrisdevito@chribis.com',
    url='https://github.com/chrisdevito/OBB',
    license="MIT",
    packages=find_packages(exclude=['tests']),
    package_data={
        '': ['LICENSE', 'README.rst', 'HISTORY.rst'],
    },
    dependency_links=dependencies,
    include_package_data=True,
    zip_safe=False,
    keywords='OBB',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
)
