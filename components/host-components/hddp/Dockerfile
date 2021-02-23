FROM python:3.8.6-slim-buster

ENV TZ Europe/Amsterdam

# Install applications so we can use them for debugging
RUN applications="bash \
                  python3-dev \
                  tzdata \
                  curl \
                  gcc \
                  git \
                  tar \
                  gawk" && \
    apt-get update -y && \
    apt-get install  -y ${applications}

# Create directories used by applications
RUN mkdir -p /backend/server
ADD server/requirements.txt /backend/server/requirements.txt
RUN pip3 install --upgrade pip \
    && pip3 install --no-cache-dir -r /backend/server/requirements.txt && rm /backend/server/requirements.txt

ADD server/backend /backend/server/backend

WORKDIR /backend/

ENV PYTHONPATH /backend/server:/usr/local/lib/python3.7/site-packages:/usr/lib/python3.7/site-packages
ENV DOCKER_HOST "172.17.0.1:2375"

EXPOSE 5000

CMD ["python3", "/backend/server/backend/main.py"]
