#!/usr/bin/env python

import os
from setuptools import find_packages, setup

install_requires = [
    line.rstrip() for line in open(
      os.path.join(os.path.dirname(__file__), "REQUIREMENTS.txt")
    )
]

setup(name='pointannotator',
      install_requires=install_requires,
      version='0.0.1',
      description='A simple GUI for annotating points in images',
      url='https://github.com/kevinyamauchi/PointAnnotator',
      author='Kevin Yamauchi',
      author_email='kevin.yamauchi@gmail.com',
      license='GPL',
      packages=find_packages(),
      zip_safe=False)
