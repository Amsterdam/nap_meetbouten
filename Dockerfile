FROM amsterdam/python
MAINTAINER datapunt@amsterdam.nl

ENV PYTHONUNBUFFERED 1
ARG BAG_OBJECTSTORE_PASSWORD
ENV BAG_OBJECTSTORE_PASSWORD=$BAG_OBJECTSTORE_PASSWORD

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
