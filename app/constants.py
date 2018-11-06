import os
from django.core.exceptions import ImproperlyConfigured

try:
    FOOTBALL_DATA_KEY = os.environ.get('FOOTBALL_DATA_KEY')
    MATCHDAY_SERVER_KEY = os.environ.get('MATCHDAY_SERVER_KEY')
except KeyError:
    error_msg = "cannot find environment variable"
    raise ImproperlyConfigured(error_msg)
