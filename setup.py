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

requirements = [str(ir.req) for ir in parse_requirements('requirements/common.txt')]

setup(
    name='cvmfs-stratum-uploader',
    version=VERSION,
    author=u'Michal Knapik',
    author_email='Michal.Knapik@stfc.ac.uk',
    package_dir={base_name: base_name},
    packages=find_packages(exclude=["*.tests"]), # include all packages under this directory
    scripts=['manage-cvmfs-stratum-uploader.py'],
    include_package_data=True,
    url='git://github.com/stfc/cvmfs-stratum-uploader.git',
    license='Apache License',
    description='Provides interface for uploading and distributing software through cvmfs repositories.',
    long_description="""Provides interface for uploading and distributing software through cvmfs repositories.

Uses Certificate Authentication provided by Apache `httpd` web server (or others).""",
    zip_safe=False,
    keywords=['cvmfs', 'django', 'uploader', 'vo', 'cern', 'stfc', 'ral', 'stratum'],
    # Adds dependencies
    install_requires=requirements,
)
