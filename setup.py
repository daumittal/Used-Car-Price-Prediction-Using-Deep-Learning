from setuptools import setup, find_packages
from typing import List

# Project Metadata
PROJECT_NAME = "Car-Price-Predictor"
VERSION = "0.0.1"
AUTHOR = "Dau Mittal"
DESCRIPTION = "A machine learning project to estimate used car prices."

# Requirements File Configuration
REQUIREMENTS_FILE = "requirements.txt"
EDITABLE_INSTALL_MARKER = "-e ."


def get_requirements() -> List[str]:
    """
    Reads the requirements.txt file and returns a list of dependencies.

    Returns:
        List[str]: A list of library names required for the project.
    """
    try:
        with open(REQUIREMENTS_FILE, "r") as file:
            requirements = file.readlines()
            # Remove newline characters and filter out the editable install marker
            requirements = [req.strip() for req in requirements if req.strip() != ""]
            if EDITABLE_INSTALL_MARKER in requirements:
                requirements.remove(EDITABLE_INSTALL_MARKER)
        return requirements
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{REQUIREMENTS_FILE}' was not found.")
    except Exception as e:
        raise Exception(f"An error occurred while reading requirements: {e}")


setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    packages=find_packages(),  # Automatically finds all packages in the project
    install_requires=get_requirements(),  # Dynamically fetches dependencies
)