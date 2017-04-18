#! /usr/bin/env python
#
# Copyright (C) 2017 Xencio <mtang024@163.com>
#
# License: Apache License

"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='xenSplittingService',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.0.1',

    description='The splitting service splitting company names '
                  'and bill memos is designed for Xencio',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/mingotang/xenSplittingService',

    # Author details
    author='The Xencio developers',
    author_email='mtang024@163.com',

    # Choose your license
    license='Apache License',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='xencio,wordsplit,service',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['docs', 'tests']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'jieba>=0.38'
    ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
    #     'data': ['check-manifest'],
    #     'test': ['tests_require'],
    # },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        'sample': ['package_data.dat'],
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'sample=sample:main',
        ],
    },
)

# ref ----------------------------------------- ref
# import codecs
# import os
# import re
# import sys
#
# from setuptools import setup, find_packages
# from setuptools.command.test import test as TestCommand
#
# here = os.path.abspath(os.path.dirname(__file__))
#
#
# class PyTest(TestCommand):
#
#     def finalize_options(self):
#         TestCommand.finalize_options(self)
#
#         self.test_args = []
#         self.test_suite = True
#
#     def run_tests(self):
#         #import here, cause outside the eggs aren't loaded
#         import pytest
#
#         sys.exit(pytest.main(self.test_args))
#
#
# def read(*parts):
#     # intentionally *not* adding an encoding option to open
#     # see here: https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
#     return codecs.open(os.path.join(here, *parts), 'r').read()
#
#
# def find_version(*file_paths):
#     version_file = read(*file_paths)
#     version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
#                               version_file, re.M)
#     if version_match:
#         return version_match.group(1)
#     raise RuntimeError("Unable to find version string.")
#
# long_description = "\n" + "\n".join([read('PROJECT.txt'),
#                                      read('docs', 'quickstart.rst')])
#
# tests_require = ['pytest', 'virtualenv>=1.10', 'scripttest>=1.3', 'mock']
#
# setup(name="pip",
#       version=find_version('pip', '__init__.py'),
#       description="A tool for installing and managing Python packages.",
#       long_description=long_description,
#       classifiers=[
#           'Development Status :: 5 - Production/Stable',
#           'Intended Audience :: Developers',
#           'License :: OSI Approved :: MIT License',
#           'Topic :: Software Development :: Build Tools',
#           'Programming Language :: Python :: 2',
#           'Programming Language :: Python :: 2.6',
#           'Programming Language :: Python :: 2.7',
#           'Programming Language :: Python :: 3',
#           'Programming Language :: Python :: 3.1',
#           'Programming Language :: Python :: 3.2',
#           'Programming Language :: Python :: 3.3',
#       ],
#       keywords='easy_install distutils setuptools egg virtualenv',
#       author='The pip developers',
#       author_email='python-virtualenv@groups.google.com',
#       url='https://pip.pypa.io/',
#       license='MIT',
#       packages=find_packages(exclude=["contrib", "docs", "tests*"]),
#       package_data={
#           'pip._vendor.requests': ['*.pem'],
#           'pip._vendor.distlib._backport': ['sysconfig.cfg'],
#           'pip._vendor.distlib': ['t32.exe', 't64.exe', 'w32.exe', 'w64.exe'],
#       },
#       entry_points=dict(console_scripts=['pip=pip:main', 'pip%s=pip:main' % sys.version[:1],
#           'pip%s=pip:main' % sys.version[:3]]),
#       tests_require=tests_require,
#       zip_safe=False,
#       extras_require={
#           'testing': tests_require,
#       },
#       cmdclass = {'test': PyTest},
# )
