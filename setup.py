#!/usr/bin/env python
import os.path

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

req_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "requirements.txt")

__version__ = open("./VERSION", "r").read().strip()

with open("README.md", "r") as fh:
    long_description = fh.read()

with open(req_path) as f:
    requires = f.read().splitlines()

extra_reqs = {
    "test": ["pytest"],
}

setup(
    name="stac_validator",
    version=__version__,
    author="James Banting",
    author_email="jbanting@sparkgeo.com",
    description="A package to validate STAC files",
    license="MIT",
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    keywords="STAC validation raster",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sparkgeo/stac-validator",
    install_requires=requires,
    extras_require=extra_reqs,
    packages=["stac_validator"],
    entry_points={
        "console_scripts": ["stac_validator = stac_validator.stac_validator:main"]
    },
)
