"""
many kids presented their own json field, this is how to do it right
hopefully some similar solution will be integrated in django
"""

__all__ = ("JSONField", )

from django.conf import settings


def JSONField(*args, database="default", **kwargs):
    engine = settings.DATABASES[database]["ENGINE"]
    if engine == 'django.db.backends.postgresql':
        from django.contrib.postgres.fields import JSONField as result
    elif engine == 'django.db.backends.mysql':
        from django_mysql.models import JSONField as result
    else:
        import json
        from django.db import models

        # add simple json field from django tickets
        # credits to https://code.djangoproject.com/ticket/29077

        class result(models.TextField):
            __qualname__ = "JSONField"
            __name__ = "JSONField"
            """ JSON field implementation on top of django textfield """

            def to_dict(self, value):
                """ convert json string to python dictionary """
                return json.loads(value)

            def to_json(self, value):
                """ convert python dictionary to json string """
                return json.dumps(value)

            def from_db_value(self, value, expression, connection):
                """ convert string from db to python dictionary """
                if value is None:
                    return value
                return self.to_dict(value)

            def to_python(self, value):
                """ convert model input value to python dictionary """
                if isinstance(value, dict):
                    return value
                if value is None:
                    return value
                return self.to_dict(value)

            def get_prep_value(self, value):
                """convert python dictionary to string before writing to db"""
                return self.to_json(value)
    return result(*args, **kwargs)
