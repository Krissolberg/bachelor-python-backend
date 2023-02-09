from setuptools import setup, find_packages

setup(
    name='bachelorbackend',
    version='1.1.1',
    package=find_packages(),
    install_requires=[
        'fastAPI',
        'shodan',
        'dotenv'
        ],
)