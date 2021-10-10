#!/usr/bin/env python
from setuptools import setup

setup(
    name="tap-gocardless",
    version="0.1.3",
    description="Singer.io tap for extracting data",
    author="morrislaptop",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_gocardless"],
    install_requires=[
        # NB: Pin these to a more specific version for tap reliability
        "singer-python",
        "requests",
    ],
    entry_points="""
    [console_scripts]
    tap-gocardless=tap_gocardless:main
    """,
    packages=["tap_gocardless"],
    package_data = {
        "schemas": ["tap_gocardless/schemas/*.json"]
    },
    include_package_data=True,
)
