# Overview

[![Release](https://github.com/pennsignals/yamlenv/workflows/release/badge.svg)](https://github.com/pennsignals/yamlenv/actions?query=workflow%3Arelease)

[![Test](https://github.com/pennsignals/yamlenv/workflows/test/badge.svg)](https://github.com/pennsignals/yamlenv/actions?query=workflow%3Atest)

* Free software: MIT license

## Install

    pip install "."

## Develop, Lint & Test

Setup:

    python3.9 -m venv .venv

    . .venv/bin/activate
    pip install ".[all]"
    pre-commit install


## Docker, Lint & Test

    docker-compose up test
