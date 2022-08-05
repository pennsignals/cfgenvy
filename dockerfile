ARG PYTHON_VERSION="3.10"
ARG ROOT_CONTAINER=python:${PYTHON_VERSION}-slim-bullseye


FROM ${ROOT_CONTAINER} as binaries
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
USER root
WORKDIR /tmp
ENV DEBIAN_FRONTEND noninteractive
RUN \
    apt-get -qq update --yes && \
    apt-get -qq upgrade --yes && \
    apt-get -qq install --yes --no-install-recommends \
	git \
        gcc \
        libc6-dev \
        libyaml-dev \
        tini \
    > /dev/null && \
    apt-get -qq clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install -U pip setuptools wheel
ENTRYPOINT ["/usr/bin/tini", "-g", "--"]


FROM binaries as source
COPY . .


FROM source as pre-commit
RUN \
    pip install ".[dev]"
CMD pre-commit run --all-files


FROM source as pytest
RUN \
    pip install ".[dev]"
CMD pytest


FROM source as build-wheel
CMD pip wheel --no-deps -w ./dist .


FROM binaries as install-wheel
CMD pip install --find-links=./dist cfgenvy[all]
