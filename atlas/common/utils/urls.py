def includer(parent_path):
    from django.urls import include as __include__
    return lambda app_name: __include__('%s.%s.urls' % (parent_path, app_name))
