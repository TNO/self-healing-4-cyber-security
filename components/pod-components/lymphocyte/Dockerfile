FROM ci.tno.nl/self-healing/common/python:master as python_shared_common

FROM python:3.8-slim-buster

ENV TZ Europe/Amsterdam

# Install applications so we can use them for debugging
RUN applications="bash \
                  tzdata \
                  curl \
                  git" && \
    apt-get update -y && \
    apt-get install  -y -qq ${applications}

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt && rm requirements.txt

COPY --from=python_shared_common /common /common
RUN cd /common && python3 setup.py install

COPY lymphocyte lymphocyte
ENV PYTHONPATH="${PYTHONPATH}:/lymphocyte"
ENV PYTHONUNBUFFERED=1

CMD ["python", "/lymphocyte/main.py"]