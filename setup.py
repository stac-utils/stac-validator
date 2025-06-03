#!/usr/bin/env python

from setuptools import setup

__version__ = "3.8.0"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="stac_validator",
    version=__version__,
    author="James Banting, Jonathan Healy",
    author_email="jonathan.d.healy@gmail.com",
    description="A package to validate STAC files",
    license="Apache-2.0",
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    keywords="STAC validation raster",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stac-utils/stac-validator",
    install_requires=[
        "requests>=2.32.3",
        "jsonschema>=4.23.0",
        "click>=8.1.8",
        "stac-pydantic>=3.3.0",
        "referencing>=0.35.1",
        "pyYAML>=6.0.1",
    ],
    extras_require={
        "dev": [
            "pytest",
            "requests-mock",
            "types-setuptools",
        ],
    },
    packages=["stac_validator"],
    entry_points={
        "console_scripts": ["stac-validator = stac_validator.stac_validator:main"]
    },
    python_requires=">=3.8",
    tests_require=["pytest", "requests-mock"],
)
