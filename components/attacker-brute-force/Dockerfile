FROM python:3.7.4-alpine3.10

RUN mkdir -p /sh4cs/attacker/
WORKDIR /sh4cs/attacker

ADD requirements.txt /sh4cs/attacker/requirements.txt

RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev gcc musl-dev build-base  \
    && pip3 install --upgrade pip \
    && pip3 install -r /sh4cs/attacker/requirements.txt \
    && apk del build-dependencies  \
    && rm /sh4cs/attacker/requirements.txt \
    && apk add bash

COPY attacker /sh4cs/attacker

ENTRYPOINT ["/bin/bash", "-c", "/usr/local/bin/python3 /sh4cs/attacker/brute_forcer.py  \"$@\"", "--"]