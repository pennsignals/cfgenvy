## Overview

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![Release](https://github.com/pennsignals/cfgenvy/workflows/release/badge.svg)](https://github.com/pennsignals/cfgenvy/actions?query=workflow%3Arelease)

[![Test](https://github.com/pennsignals/cfgenvy/workflows/test/badge.svg)](https://github.com/pennsignals/cfgenvy/actions?query=workflow%3Atest)

Keep secrets out of env variables in production by using env files. Merge env files into configuration dynamically. Keep env file and env variable handling out of the application by making application dependent only on the configuration file. Prefer deserilization from yaml over configuration of partially initialized objects.

An argument parser that accepts:
* A required yaml file for configuration/deserialization.
* An optional env file for secrets.

Features:
* MIT license
* Interpolate environment variables directly into yaml configuration.
* Optional replacement of environment variables with an environment variable file.
* Use C Yaml safe load/dump or yaml safe load/dump.
* Pass in env to parser with os.environ as a default.
* Pass in argv to parser with sys.argv[1:] as a default.
* Yaml type registration functions.

Relative configargparse, python-dotenv, envyaml, and yamlenv:
* Dependency injection through depth-first deserialization of yaml is better than two-pass, breadth-first initialization followed by a configuration.
* Contract for env variables is between configuration file and env xor the env file, the app no longer cares much about env or secrets as it uses the interpolated configuration file.
* No ${MY_VAR:my-default} --unexpected env var syntax for default values, an expensive pattern match, and allows typos of MY_VAR to pass silently--.
* No "N/A" or null default when environment variable does not exist --allows configuration errors to pass silently to become runtime errors--.
* Env file is optional, but when provided it does not merge with existing environment variables --better tracability in production deployment--.
* Yaml type registration retains the registered yaml tag in a closure.
* Env yaml type registration retains the registered env variable set in a closure.

## Install

    pip install "."

## Develop, Lint & Test

Setup:

    python3.10 -m venv .venv
    . .venv/bin/activate
    pip install ".[all]"
    pre-commit install
    pre-commit run --all-files

    ...

    deactivate


## Docker, Lint & Test

    docker compose run test
    docker compose run pre-commit
    docker compose run test-wheel-install
