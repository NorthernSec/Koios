from django.urls import path
from csp_report  import views

app_name = "csp-report"

urlpatterns = [
    path('', views.csp_report, name='csp_report'),
]
