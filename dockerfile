ARG PYTHON_VERSION="3.10"

FROM python:${PYTHON_VERSION}-slim-bullseye as binaries
ARG TINI_VERSION=v0.19.0
WORKDIR /tmp
ENV PATH /root/.local/bin:$PATH
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN \
    chmod +x /usr/bin/tini && \
    apt-get -qq update --fix-missing && \
    apt-get -qq install -y --no-install-recommends git libyaml-dev > /dev/null && \
    apt-get -qq clean && \
    apt-get -qq autoremove -y --purge && \
    rm -rf /var/lib/apt/lists/*
ENTRYPOINT [ "/usr/bin/tini", "--" ]

FROM binaries as wheel
COPY . .
RUN \
    pip install -U pip setuptools build wheel
CMD pip wheel --no-deps -w ./dist .

FROM wheel as pre-commit
RUN \
    pip install ".[all]"
CMD pre-commit run --all-files

FROM wheel as test
RUN \
    pip install ".[all]"
CMD pytest

FROM wheel as build-wheel-install
RUN \
    pip wheel --no-deps -w ./dist .

FROM binaries as test-wheel-install
COPY --from=build-wheel-install /tmp/dist/*.whl /tmp/dist/
RUN \
    pip install --find-links=./dist cfgenvy[all]
