FROM ci.tno.nl/self-healing/common/python:master as python_shared_common

FROM php:7-fpm

RUN apt-get update && apt install -y git python3 python3-pip
ADD requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

COPY --from=python_shared_common /common /common
RUN cd /common && python3 setup.py install

ADD code /code
ADD startup.sh /startup.sh
ADD redis4php.py /redis4php.py

WORKDIR /code

CMD ["/bin/bash", "/startup.sh"]