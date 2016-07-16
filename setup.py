#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os

from setuptools import find_packages, setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


version = '0.9.9'

setup(
    name='pytest-nodev',
    version=version,
    author='Alessandro Amici',
    author_email='alexamici@gmail.com',
    license='MIT',
    url='http://pytest-nodev.readthedocs.io',
    download_url='https://github.com/nodev-io/pytest-nodev/archive/%s.tar.gz' % version,
    description="Test-driven source code search for Python.",
    long_description=read('README.rst'),
    packages=find_packages(),
    install_requires=[
        'future',
        'pytest>=2.8.1',
        'pytest-timeout',
    ],
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Framework :: Pytest',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='test-driven source code search plugin pytest nodev',
    entry_points={
        'pytest11': [
            'nodev = pytest_nodev.plugin',
        ],
    },
)
