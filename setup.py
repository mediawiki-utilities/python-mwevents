import os
from distutils.core import setup

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def requirements(fname):
    for line in open(os.path.join(os.path.dirname(__file__), fname)):
        yield line.strip()


setup(
    name='mwevents',
    version=read('VERSION').strip(),
    author='Aaron Halfaker',
    author_email='aaron.halfaker@gmail.com',
    packages=find_packages(),
    scripts=[],
    url='http://pypi.python.org/pypi/mwevents',
    license=open('LICENSE').read(),
    description='Standardized public MediaWiki events for tools and Science.',
    long_description=read('README.rst'),
    install_requires=requirements('requirements.txt'),
    test_suite='nose.collector',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: General",
        "Topic :: Utilities",
        "Topic :: Scientific/Engineering"
    ],
)
