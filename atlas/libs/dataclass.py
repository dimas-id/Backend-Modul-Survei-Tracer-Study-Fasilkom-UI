from django.db.models import Manager
from decimal import Decimal
from uuid import UUID


class DataClass:

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    @classmethod
    def from_object(cls, obj, **kwargs):
        return cls(
                **{
                    field: kwargs.get(field, getattr(obj, field, None))
                    for field in cls.Meta.fields
                }
        )

    def to_dict(self):
        dictionary = {field: self._to_repr(self._get_value(field))
                      for field in self.Meta.fields}
        return dictionary

    def _get_value(self, field):
        if not hasattr(self, field):
            return None
        return getattr(self, field)

    def _to_repr(self, val):
        if isinstance(val, list):
            return [self._to_repr(element) for element in val]
        elif isinstance(val, Decimal):
            return float(val)
        elif isinstance(val, UUID):
            return str(val)
        elif isinstance(val, DataClass):
            return val.to_dict()
        elif isinstance(val, Manager):
            return [str(v) for v in val.all()]
        return val

    class Meta:
        fields = ()
