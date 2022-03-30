# -*- coding: utf-8 -*-
"""cfgenvy: Cfg Env Yaml."""

from setuptools import find_packages, setup

INSTALL_REQUIRES = (
    "pip>=22.0.4",
    "pyyaml>=5.3.1",
    "setuptools>=61.2.0",
    "setuptools_scm[toml]>=6.4.2",
    "wheel>=0.37.1",
)

TEST_REQUIRES = (
    "astroid",
    "black",
    "coverage[toml]",
    "flake8",
    "flake8-bugbear",
    "flake8-commas",
    "flake8-comprehensions",
    "flake8-docstrings",
    "flake8-logging-format",
    "flake8-mutable",
    "flake8-sorted-keys",
    "isort",
    "mypy",
    "pep8-naming",
    "pre-commit",
    "pylint",
    "pytest",
    "pytest-cov",
    "types-pkg-resources",
    "types-pyyaml",
)

setup(
    extras_require={
        "all": TEST_REQUIRES,
        "test": TEST_REQUIRES,
    },
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    use_scm_version={"local_scheme": "dirty-tag"},
)
