""" Setup file.
"""
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()


requires = [
    'cornice',
    'Sphinx',
    'docutils'
]

setup(name='cornice_sphinx',
    version=0.1,
    description='Generate Sphinx documentation from a Cornice application',
    long_description=README,
    license='Apache License (2.0)',
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
    ],
    keywords="web services",
    author='Mozilla Services and contributors',
    author_email='services-dev@mozilla.org',
    url='https://github.com/Cornices/cornice.ext.sphinx',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
)
