#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

from setuptools import setup

install_requirements = [
    "django"
]

setup(name='django-simple-jsonfield',
      version="0.3.1",
      install_requires=install_requirements,
      license="Public Domain",
      url="http://github.org/devkral/django-simple-jsonfield/",
      zip_safe=True,
      platforms='Platform Independent',
      packages=[
        "jsonfield"
      ],
      test_suite="tests")
