import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from pprint import pprint

IGNORE_SOURCE_FILES = [
    'sandbox eval code',
    'moz-extension'
]

@csrf_exempt
@require_http_methods(["POST"])
def csp_report(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception as e:
        #TODO: Logging
        return HttpResponse(status=500)
    if data.get('csp-report', {}).get("source-file", '').lower() in IGNORE_SOURCE_FILES:
        #TODO: Logging (debug)
        return HttpResponse(status=204)
    pprint(data)
    return HttpResponse(status=204)
