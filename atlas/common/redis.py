import django_rq

__default__ = django_rq.get_queue('default')

def enqueue(func, *args, **kwargs):
    __default__.enqueue(func, *args, **kwargs)

