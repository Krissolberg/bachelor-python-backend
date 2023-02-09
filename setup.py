from setuptools import setup, find_packages

setup(
    name='bachelor-backend',
    version='1.1.1',
    package=find_packages(),
    install_requires=[
        'Twisted<=15.2.1'
        ],
)