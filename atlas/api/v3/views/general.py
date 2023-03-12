from django.http import HttpResponse

# hello message from atlas v3 :)
def api_v3(request):
    return HttpResponse(content='Hello from Atlas v3')
