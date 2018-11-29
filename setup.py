#!/usr/bin/env python
import sys
import os.path

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

req_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "requirements.txt")
version = open("./VERSION", "r").read().strip()
with open("README.md", "r") as fh:
    long_description = fh.read()

with open(req_path) as f:
    requires = f.read().splitlines()

setup(
    name="stac_validator",
    version="0.0.1",
    author="James Banting",
    author_email="jbanting@sparkgeo.com",
    description="A package to validate STAC items and catalogs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requires,
    packages=["stac_validator"],
    entry_points={
        'console_scripts': [
            'stac_validator = stac_validator.stac_validator:main'
        ]
    },
    tests_require=["pytest"],
)
