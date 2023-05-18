from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="loquax",
    version="0.1.0",
    author="Matthieu Court",
    author_email="matthieu.court@protonmail.com",
    description="A Classical Phonology framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mattlianje/loquax",
    packages=find_packages(exclude=['tests', 'tests.*']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires='>=3.10',
)