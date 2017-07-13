#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

reqs = [line for line in open('requirements/base.txt').read().split("\n")]

readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://wordpress-to-staticman.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='wordpress-to-staticman',
    version='0.1.0',
    description='Convert WordPress comments to Staticman comments',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Jess Johnson',
    author_email='jess@grokcode.com',
    url='https://github.com/grokcode/wordpress-to-staticman',
    packages=[
        'wp2staticman',
    ],
    package_dir={'wordpress-to-staticman': 'wp2staticman'},
    include_package_data=True,
    install_requires=reqs,
    license='MIT',
    zip_safe=False,
    keywords='wordpress-to-staticman',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
