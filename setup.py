# Always prefer setuptools over distutils
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

setup(
    name="async-worker",
    version="0.11.0",
    description="Microframework para escrever workers assíncronos em Python",
    long_description="Microframework para escrever workers assíncronos em Python",
    url="https://github.com/B2W-BIT/async-worker",
    # Author details
    author="Dalton Barreto",
    author_email="daltonmatos@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    install_requires=[
        "aioamqp==0.12.0",
        "aiologger>=0.4.0-rc1",
        "pydantic==0.30",
        "cached-property==1.5.1",
        "aiohttp==3.4.4",
    ],
    entry_points={},
)
