import json
import logging

from django.http                  import HttpResponse, JsonResponse
from django.shortcuts             import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from koios_admin.settings import CSP_EXCEMPT_SOURCE_FILES

logger = logging.getLogger("koios.admin")

@csrf_exempt
@require_http_methods(["POST"])
def csp_report(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception as e:
        logger.error(
            f"Error during CSP report decoding: {e.name}",
            extra={'error': e, 'view': 'csp_report'}
        )
        return HttpResponse(status=500)

    report_source = data.get('csp-report', {}).get("source-file", '')
    if report_source.lower() in CSP_EXCEMPT_SOURCE_FILES:
        logger.debug(
            f"CSP-excempt report logged",
            extra={'source': report_source, 'view': 'csp_report', 'report': data}
        )
        return HttpResponse(status=204)
    logger.warning(
        f"CSP-report logged",
        extra={'source': report_source, 'view': 'csp_report', 'report': data}
    )
    return HttpResponse(status=204)


# ----
# Debug Views
# ----

def health_check(request):
    return JsonResponse({"status": "ok"})


def debug_csp_report(request):
    return render(request, "koios_admin/debug_csp-report-trigger.html")
