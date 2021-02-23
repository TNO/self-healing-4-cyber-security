FROM ci.tno.nl/self-healing/common/python:master as python_shared_common

FROM python:alpine

RUN apk update && apk add git
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY --from=python_shared_common /common /common
RUN cd /common && python3 setup.py install

COPY channel_frequency_monitor channel_frequency_monitor
ENV PYTHONPATH="${PYTHONPATH}:/channel_frequency_monitor"
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "/channel_frequency_monitor/main.py"]
