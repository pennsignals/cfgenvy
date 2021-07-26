# Overview

An argument parser that accepts:
* A required yaml file for configuration/deserialization.
* An optional env file for secrets.

Features:
* MIT license
* Interpolate environment variables directly into yaml configuration.
* Replace environment variables with an environment variable file.
* Use C Yaml safe load/dump or yaml safe load/dump.
* Pass in env to parser with os.environ as a default.
* Pass in argv to parser with sys.argv[1:] as a default.
* Yaml type registration functions

Relative configargparse, python-dotenv, and yamlenv:
* Deserialization and yaml file format is better than (post) configuration.
* Contract for env variables is between configuration file and env, the app no longer has to care much about env or secrets.
* No ${MY_VAR:my-default} --unexpected env var syntax--.
* No "N/A" or null default when environment variable does not exist --do not allow configuration errors to look like runtime errors--.
* Env file is optional.

## Status

[![Release](https://github.com/pennsignals/envyaml/workflows/release/badge.svg)](https://github.com/pennsignals/envyaml/actions?query=workflow%3Arelease)

[![Test](https://github.com/pennsignals/envyaml/workflows/test/badge.svg)](https://github.com/pennsignals/envyaml/actions?query=workflow%3Atest)

## Install

    pip install "."

## Develop, Lint & Test

Setup:

    python3.9 -m venv .venv

    . .venv/bin/activate
    pip install ".[all]"
    pre-commit install


## Docker, Lint & Test

    docker-compose run test
