FROM nginx:1.17.8 AS base-cert

RUN apt update && apt install openssl

RUN mkdir -p /certs
RUN openssl req -x509 -nodes -days 365 -subj "/C=PE/ST=Lima/L=Lima/O=Acme Inc. /OU=IT Department/CN=nginx.local" -addext "subjectAltName = DNS:localhost" -newkey rsa:2048 -keyout /certs/privkey.pem -out /certs/fullchain.pem

FROM nginx:1.17.8

ADD nginx.conf /etc/nginx/nginx.conf
ADD code /code

COPY --from=base-cert /certs /certs
EXPOSE 443
ENV TZ "Europe/Amsterdam"
