"""
URL configuration for koios project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from importlib        import import_module
from django.conf      import settings
from django.contrib   import admin
from django.urls      import path
from django.urls.conf import include, re_path
from tastypie.api     import Api

from koios.functions  import get_projects
from koios.classes    import AuthenticatedResource

# Base URL's
urlpatterns = [
    path('admin/', admin.site.urls),
]

# Load project URLs - Views
for project in get_projects():
    urlpatterns.append( path(project+"/", include(project+".urls")) )

# Load project URLs - API
# v1 API
v1_api = Api(api_name="v1")

for app in settings.INSTALLED_APPS:
    try:
        api_module = import_module(f"{app}.api")
    except ModuleNotFoundError:
        continue  # app has no api.py, skipping

    for attr_name in dir(api_module):
        attr = getattr(api_module, attr_name)
        if (isinstance(attr, type)
            and issubclass(attr, AuthenticatedResource)
            and attr is not AuthenticatedResource):
            v1_api.register(attr())
urlpatterns.append( re_path(r"^api/", include(v1_api.urls)) )
