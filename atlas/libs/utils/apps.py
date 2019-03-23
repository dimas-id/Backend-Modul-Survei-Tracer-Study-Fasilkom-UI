from django.apps import apps

def get_app_path(app_name):
    return 'atlas.apps.%s' % app_name

def get_model_path(app_name, model_name):
    return '%s.%s' % (get_app_path(app_name), model_name)

def get_model(app_name, model_name):
    app_path = get_app_path(app_name)
    return apps.get_model(app_path, app_name)