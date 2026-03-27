
from importlib            import import_module
from django.conf          import settings
from django.contrib       import admin
from django.urls          import path
from django.urls.conf     import include, re_path
from django.views.generic import RedirectView
from tastypie.api         import Api

from koios.functions  import get_projects, get_plugin_app
from koios.classes    import AuthenticatedResource, AuthenticatedModelResource
from koios.settings   import LANDINGPAGE

# Base URL's
urlpatterns = [
    path('admin/', admin.site.urls),
]
if LANDINGPAGE:
    urlpatterns.append(
        path('', RedirectView.as_view(pattern_name=LANDINGPAGE, permanent=False))
    )

# Load project URLs - Views
for project in get_projects():
    try:
        app  = get_plugin_app(project)
        slug = (app.plugin_meta.get('url_slug') or project).rstrip("/")
        urlpatterns.append( path(slug+"/", include(project+".urls")) )
    except ModuleNotFoundError:
        print("No URLs found for "+project)
    except Exception as e:
        print(f"[!] Error importing {project}: {e}")

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
            and issubclass(attr, (AuthenticatedResource, AuthenticatedModelResource))
            and attr is not AuthenticatedResource
            and attr is not AuthenticatedModelResource):
            v1_api.register(attr())
urlpatterns.append( re_path(r"^api/", include(v1_api.urls)) )
