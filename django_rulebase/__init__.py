import os
if "DJANGO_SETTINGS_MODULE" not in os.environ:
    raise Exception("django is missing")

from .request import Request
from .validator import Validator
from .rule import Rule