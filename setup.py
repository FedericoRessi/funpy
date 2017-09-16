import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(
    name="funpy",
    version="0.0.0",
    author="Federico Ressi",
    description="Python funtional programming tools for numeric data.",
    license="BSD",
    keywords="numpy functional",
    url="http://packages.python.org/an_example_pypi_project",
    packages=['funpy'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
