FROM amsterdam/python:3.9-buster
MAINTAINER datapunt@amsterdam.nl

ENV PYTHONUNBUFFERED 1
ARG GOB_OBJECTSTORE_PASSWORD
ENV GOB_OBJECTSTORE_PASSWORD=$GOB_OBJECTSTORE_PASSWORD

EXPOSE 8000
WORKDIR /app/
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /static && chown datapunt /static

ENV DJANGO_SETTINGS_MODULE=nap_meetbouten.settings.docker

COPY nap_meetbouten /app/
COPY .jenkins-import /.jenkins-import/

USER datapunt

RUN ./manage.py collectstatic

CMD ["/app/docker-run.sh"]
