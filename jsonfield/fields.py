"""
    a jsonfield which uses available jsonfields
    hopefully some similar solution will be integrated in django
"""

__all__ = ("JSONField", "FallbackJSONField")


import json

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


# add simple json field from django tickets
# credits to https://code.djangoproject.com/ticket/29077
class FallbackJSONField(models.TextField):
    __qualname__ = "JSONField"
    __name__ = "JSONField"
    """ JSON field implementation on top of django textfield """

    def to_dict(self, value):
        """ convert json string to python dictionary """
        try:
            return json.loads(value)
        except json.decoder.JSONDecodeError as e:
            raise ValidationError(
                message="Error: %(error)s. Value: %(value)s",
                code="json_error",
                params={"error": e, "value": value}
            )

    def to_json(self, value):
        """ convert python dictionary to json string """
        # force parsing of strings into correct json structures
        if isinstance(value, str):
            value = self.to_dict(value)
        return json.dumps(value)

    def from_db_value(self, value, expression, connection):
        """ convert string from db to python dictionary """
        if value is None:
            return value
        return self.to_dict(value)

    def to_python(self, value):
        """ convert model input value to python dictionary """
        if isinstance(value, (dict, list)):
            return value
        if value is None:
            return value
        return self.to_dict(value)

    def value_to_string(self, obj):
        """use python dictionary for serializing"""
        value = self.value_from_object(obj)
        return value

    def get_prep_value(self, value):
        """convert python dictionary to json before writing to db"""
        return self.to_json(value)


def JSONField(*args, database="default", **kwargs):
    engine = settings.DATABASES[database]["ENGINE"]
    if engine == 'django.db.backends.postgresql':
        from django.contrib.postgres.fields import JSONField as result
        result.__name__ = "JSONField"
    elif engine == 'django.db.backends.mysql':
        from django_mysql.models import JSONField as result
        result.__name__ = "JSONField"
    else:
        result = FallbackJSONField
    return result(*args, **kwargs)
