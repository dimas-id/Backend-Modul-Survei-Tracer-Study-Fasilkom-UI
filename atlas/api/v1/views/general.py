from django.http import HttpResponse

def api_v1(request, *args):
    return HttpResponse(content='Hello from Atlas v1')