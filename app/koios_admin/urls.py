from django.urls import path
from koios_admin import settings, views

app_name = 'koios_admin'

urlpatterns = [
    path('csp-report/', views.csp_report,   name='csp_report'),
    path('_health',     views.health_check, name='health_check'),
]

if settings.DEBUG_CSP:
    urlpatterns.append(
        path('debug/csp-report', views.debug_csp_report, name='debug_csp_report')
    )
