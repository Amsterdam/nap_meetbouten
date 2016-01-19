FROM python:3.5-onbuild

ENV PYTHONUNBUFFERED 1

MAINTAINER datapunt@amsterdam.nl

RUN apt-get update

RUN apt-get install -y python3-pip python3-dev

COPY atlas_nap_meetbouten /app/

CMD /app/docker-entrypoint.sh
