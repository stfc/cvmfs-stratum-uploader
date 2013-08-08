#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages
from pip.req import parse_requirements
import re
import os

base_name = 'archer'
v_file = open(os.path.join(os.path.dirname(__file__),
                           base_name, '__init__.py'))

VERSION = re.compile(r".*__version__ = '(.*?)'",
                     re.S).match(v_file.read()).group(1)

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

reqs = parse_requirements('requirements/production.txt')

setup(
    name='uploader',
    version=VERSION,
    author=u'Michal Knapik',
    author_email='Michael.Knapik@stfc.ac.uk',
    package_dir={base_name: base_name},
    packages=find_packages(), # include all packages under this directory  
    include_package_data=True,
    url='git://github.com/mknapik/uploader.git',
    license='Apache 2.0',
    description='Provides interface for uploading and distributing software through cvmfs repositories.',
    long_description=open('README.md').read(),
    zip_safe=False,
    # Adds dependencies    
    install_requires=[str(ir.req) for ir in reqs],
)