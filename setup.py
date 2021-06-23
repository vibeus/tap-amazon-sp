#!/usr/bin/env python
from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name="tap-amazon-sp",
    version="0.1.1",
    description="Singer.io tap for extracting data from Amazon Seller Partner API.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Vibe Inc",
    url="https://github.com/vibeus/tap-amazon-sp",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_amazon_sp"],
    install_requires=[
        "python-amazon-sp-api",
        "requests",
        "singer-python",
    ],
    entry_points="""
    [console_scripts]
    tap-amazon-sp=tap_amazon_sp:main
    """,
    packages=["tap_amazon_sp", "tap_amazon_sp.streams"],
    package_data={"schemas": ["tap_amazon_sp/schemas/*.json"]},
    include_package_data=True,
)
