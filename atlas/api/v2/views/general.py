from django.http import HttpResponse

def api_v2(request, *args):
    return HttpResponse(content='Hello from Atlas v2')
