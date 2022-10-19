import os
from setuptools import setup
import runpy

def read(fname):
    f = open(os.path.join(os.path.dirname(__file__), fname))
    r = f.read()
    f.close()
    return r

setup(
    name="quizlet-api",
    version=runpy.run_path("./quizlet/__version__.py")["__version__"],
    packages=["quizlet"],
    license="MIT",
    description="An unofficial API for interacting with public Quizlet sets.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="obfuscatedgenerated",
    author_email="pip@obfuscatedgenerated.ml",
    url="https://github.com/obfuscatedgenerated/quizlet-api",
    repository="https://github.com/obfuscatedgenerated/quizlet-api",
    keywords=["quizlet", "api"],
    install_requires=["requests>=2.28.1"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
