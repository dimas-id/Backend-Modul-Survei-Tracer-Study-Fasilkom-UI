from django.conf import settings
import django_rq

__default__ = django_rq.get_queue('default')


def enqueue(func, *args, **kwargs):
    if settings.TESTING:
        return
    __default__.enqueue(func, *args, **kwargs)
