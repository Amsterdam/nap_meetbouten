import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import connection

try:
    from django.apps import apps

    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model
from django.http import HttpResponse

try:
    model = get_model(settings.HEALTH_MODEL)
except:
    raise ImproperlyConfigured(
        'settings.HEALTH_MODEL doesn\'t resolve to a useable model')

log = logging.getLogger(__name__)


def health(request):
    msg = "Health OK"
    statuscode = 200

    if settings.DEBUG:
        # Check debug mode
        msg = "Debug mode not allowed in production"
        statuscode = 500
    else:
        # check database
        try:
            with connection.cursor() as cursor:
                cursor.execute("select 1")
                assert cursor.fetchone()
        except Exception as e:
            msg = "Database connectivity failed: {}".format(e.msg)
            statuscode = 500

    # Do we need to explicitly log this at all?
    if statuscode != 200:
        log.exception(msg)

    return HttpResponse(msg, content_type='text/plain', status=statuscode)


def check_data(request):
    # check bag
    try:
        assert model.objects.count() > 10
    except:
        log.exception("No BAG data found")
        return HttpResponse("No BAG data found", content_type="text/plain",
                            status=500)
