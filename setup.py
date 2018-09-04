# coding = utf-8
from setuptools import setup


setup(
    name='LBank',
    version = '1.0.1',
    packages = ['LBank'],
    author = 'lbank',
    install_requires = ['requests>=2.18.4', 'pycrypto>=2.6.1'],
    classifiers = [
        'Programming Language :: Python :: 3.6'
    ]
)
