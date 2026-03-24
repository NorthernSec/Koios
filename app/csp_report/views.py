import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def csp_report(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        print(data)
    return HttpResponse(status=204)
