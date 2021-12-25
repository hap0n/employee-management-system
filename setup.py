from os import path
from typing import List

from setuptools import setup, find_packages

try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements

FILE_DIR = path.dirname(__file__)


def extract_requirements(requirements_file: str) -> List[str]:
    requirements = list(parse_requirements(path.join(FILE_DIR, requirements_file), session=False))
    try:
        return [str(line.req) for line in requirements]
    except AttributeError:
        return [str(line.requirement) for line in requirements]


requirements = extract_requirements("requirements.txt")
dev_requirements = extract_requirements("requirements.dev.txt")


setup(
    name="employee-management-system",
    version="0.0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=requirements,
    tests_require=dev_requirements,
    extras_require={"dev": dev_requirements},
)
