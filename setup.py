#!/usr/bin/env python

import setuptools

import contacts

setuptools.setup(
    name='contacts',
    version=contacts.version,
    description='Simple contact information manager.',
    long_description=open('README.rst').read(),
    url='https://github.com/dave-shawley/contacts',
    author='Dave Shawley',
    author_email='daveshawley@gmail.com',
    packages=['contacts'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
