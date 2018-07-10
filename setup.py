from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='async-worker',
    version='0.2.1-rc2',
    description="Microframework para escrever consumers para RabbitMQ",
    long_description="Microframework para escrever consumers para RabbitMQ",
    url='https://github.com/B2W-BIT/async-worker',
    # Author details
    author='Dalton Barreto',
    author_email='daltonmatos@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires = [
        "aioamqp==0.10.0",
        "easyqueue==1.0.0",
        "simple-json-logger==0.2.3",
    ],
    entry_points={},
)
