#!/bin/python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requires = [
    "requests",
]

setuptools.setup(
    name='sunweg',
    version='0.0.5',
    author="rokam",
    author_email="lucas@mindello.com.br",
    description="A library to retrieve data from sunweg.net",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rokam/sunweg",
    install_requires=requires,
    packages=setuptools.find_packages(),
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
)