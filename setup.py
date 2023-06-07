from setuptools import setup
from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="isikukood",
    version="1.0.2",
    description="Estonian SSN library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ui-1/isikukood",
    author="ui-1",
    author_email="ui-1@posteo.org",
    license="GPLv3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries"
    ],
    packages=["isikukood"],
    include_package_data=True,
    install_requires=["multimethod"]
)
