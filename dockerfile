ARG IFLAGS="--quiet --no-cache-dir --user"
ARG PYTHON_VERSION="3.7"

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

FROM wheel as build-wheel
RUN \
    pip wheel --no-deps -w ./dist .

FROM binaries as test
COPY --from=build-wheel /tmp/dist/*.whl /tmp/dist/
RUN \
    pip install --find-links=./dist cfgenvy[all]
CMD pytest
