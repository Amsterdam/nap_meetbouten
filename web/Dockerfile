FROM python:3.5-onbuild
MAINTAINER datapunt@amsterdam.nl

ENV PYTHONUNBUFFERED 1

WORKDIR /app/atlas_nap_meetbouten
EXPOSE 8000

RUN apt-get update
RUN apt-get install -y python3-pip python3-dev libgeos-dev
RUN pip install --upgrade pip
RUN adduser --system datapunt

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

RUN pip install uwsgi
RUN mkdir /app/static && chown datapunt /app/static

USER datapunt

COPY atlas_nap_meetbouten /app/atlas_nap_meetbouten

CMD /app/atlas_nap_meetbouten/docker-entrypoint.sh
