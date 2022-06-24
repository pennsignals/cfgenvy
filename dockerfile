ARG IFLAGS="--quiet --no-cache-dir --user"

FROM python:3.10-slim-bullseye as build
ARG IFLAGS
ARG TINI_VERSION=v0.19.0
WORKDIR /tmp
ENV PATH /root/.local/bin:$PATH
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
COPY license.txt .
COPY readme.md .
COPY setup.cfg .
COPY setup.py .
COPY pyproject.toml .
COPY .pre-commit-config.yaml .
COPY .git ./.git
COPY src ./src
COPY test ./test
RUN \
    chmod +x /usr/bin/tini && \
    apt-get -qq update --fix-missing && \
    apt-get -qq install -y --no-install-recommends git libyaml-dev > /dev/null && \
    pip install ${IFLAGS} "." && \
    apt-get -qq clean && \
    apt-get -qq autoremove -y --purge && \
    rm -rf /var/lib/apt/lists/*
ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "pip", "wheel", "--no-deps", "-w", "./dist", "." ]

FROM build as test
RUN \
    pip wheel --no-deps -w ./dist . && \
    for EACH in ./dist/*.whl; do pip install ${IFLAGS} "${EACH}[all]"; done
CMD [ "pre-commit", "run", "--all-files" ]
