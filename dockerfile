ARG IFLAGS="--quiet --no-cache-dir --user"
ARG PYTHON_VERSION="3.7"

#FROM python:3.10-slim-bullseye as build
FROM python:${PYTHON_VERSION}-slim-bullseye as build
ARG IFLAGS
ARG TINI_VERSION=v0.19.0
ARG PYTHON_VERSION
WORKDIR /tmp
ENV PATH /root/.local/bin:$PATH
ENV PYTHON_VERSION ${PYTHON_VERSION}
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
COPY . .
RUN \
    pip install -U pip setuptools build wheel && \
    chmod +x /usr/bin/tini && \
    apt-get -qq update --fix-missing && \
    apt-get -qq install -y --no-install-recommends git libyaml-dev > /dev/null && \
    pip install ${IFLAGS} "." && \
    apt-get -qq clean && \
    apt-get -qq autoremove -y --purge && \
    rm -rf /var/lib/apt/lists/*
ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD python setup.py bdist_wheel --python-tag="py$(echo ${PYTHON_VERSION} | tr '.' '')"

FROM build as test
ARG PYTHON_VERSION
ARG IFLAGS
RUN \
    pip wheel --no-deps -w ./dist . && \
    for EACH in ./dist/*.whl; do pip install ${IFLAGS} "${EACH}[all]"; done
CMD pre-commit run --all-files