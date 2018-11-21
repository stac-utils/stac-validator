#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


version = open("./VERSION", "r").read().strip()
with open("README.md", "r") as fh:
    long_description = fh.read()

# Runtime requirements.
inst_reqs = [
    "requests>=2.19.1",
    "docopt>=0.6.2",
    "jsonschema>=2.6.0",
    "asks==2.2.0",
    "trio==0.9.0",
    "cachetools>=2.1.0"
]

extra_reqs = {
    "test": ["pytest>=3.8.0"]
}


setup(
    name="stac_validator",
    version=version,
    author="James Banting",
    author_email="jbanting@sparkgeo.com",
    description="A package to validate STAC items and catalogs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3",
    packages=find_packages(exclude=["tests"]),
    install_requires=inst_reqs,
    extras_require=extra_reqs,
    entry_points={
        "console_scripts": [
            "validate-stac = stac_validator.scripts.cli:main"
        ],
    },
)
