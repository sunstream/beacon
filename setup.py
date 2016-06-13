#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(name='beacon',
      version='1.0.0',
      scripts=['bin/summarize-beacon'],
      packages=find_packages(),
      install_requires=[
            'python-dateutil',
            'tzlocal'
      ]
      )
