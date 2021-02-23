FROM ci.tno.nl/self-healing/common/python:master as python_shared_common

FROM python:3.7.4-alpine3.10

RUN cd /etc/apk/keys \
    && wget http://alpine.adiscon.com/rsyslog@lists.adiscon.com-5a55e598.rsa.pub \
    && echo 'http://alpine.adiscon.com/3.7/stable' >> /etc/apk/repositories

RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev gcc musl-dev build-base \
    && pip3 install --upgrade pip \
    && apk add git bash \
    && apk del build-dependencies

RUN mkdir -p /var/log/supervisor

COPY requirements.txt /auth/requirements.txt
RUN pip install --no-cache-dir -r /auth/requirements.txt  && rm /auth/requirements.txt

COPY --from=python_shared_common /common /common
RUN cd /common && python3 setup.py install

COPY /auth /auth/auth

ENV TZ Europe/Amsterdam
EXPOSE 5000

ENV PYTHONUNBUFFERED=0

WORKDIR /auth
ENV PYTHONPATH /auth

CMD ["/usr/local/bin/python3.7", "/auth/auth/main.py"]