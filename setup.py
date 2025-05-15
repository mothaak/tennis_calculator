"""Setup script for the tennis calculator package."""

from setuptools import setup, find_packages

# Read the version from __init__.py
with open("tennis_calculator/__init__.py", "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip("\"'")
            break

# Read the long description from README.md
with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="tennis_calculator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "tennis-calculator=tennis_calculator.cli:main",
        ],
    },
    description="A package for calculating tennis match scores and statistics.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Moditha"
)
