import logging

from importlib            import import_module
from django.conf          import settings
from django.contrib       import admin
from django.urls          import path
from django.urls.conf     import include, re_path
from django.views.generic import RedirectView
from tastypie.api         import Api

from koios.functions  import get_applets, get_applet_app
from koios.classes    import AuthenticatedResource, AuthenticatedModelResource
from koios.settings   import LANDINGPAGE

logger = logging.getLogger("koios")

# Base URL's
urlpatterns = [
    path('admin/', admin.site.urls),
]
if LANDINGPAGE:
    urlpatterns.append(
        path('', RedirectView.as_view(pattern_name=LANDINGPAGE, permanent=False))
    )

# Load applet URLs - Views
for applet in get_applets():
    try:
        app  = get_applet_app(applet)
        slug = (app.applet_meta.get('url_slug') or applet).rstrip("/")
        urlpatterns.append( path(slug+"/", include(applet+".urls")) )
        logger.debug(f"Loaded URL's for {applet} under {slug}", {'applet': applet})
    except ModuleNotFoundError as e:
        if e.name == f"{applet}.urls":
            logger.warning(f"No URLs file found for {applet}", {'applet': applet})
        else:
            logger.error(
                f"Dependency missing while importing {applet}.urls: {e.name}",
                extra={'error': e, 'applet': applet}
            )
    except Exception as e:
        logger.error(f"Error importing {applet}",
                     extra={'error': e, 'applet': applet})

# Load applet URLs - API
# v1 API
v1_api = Api(api_name="v1")

for app in get_applets():
    try:
        api_module = import_module(f"{app}.api")
    except ModuleNotFoundError as e:
        if e.name == f"{app}.api":
            logger.debug(f"No URLs file found for {applet}", {'applet': applet})
        else:
            logger.error(
                f"Dependency missing while importing {applet}.urls: {e.name}",
                extra={'error': e, 'applet': applet}
            )
        continue

    for attr_name in dir(api_module):
        attr = getattr(api_module, attr_name)
        if (isinstance(attr, type)
            and issubclass(attr, (AuthenticatedResource,
                                  AuthenticatedModelResource))
            and attr is not AuthenticatedResource
            and attr is not AuthenticatedModelResource):
            logger.debug(f"Loading {attr._meta.resource_name} from {app}",
                         extra={'applet': app,
                                'resource': attr._meta.resource_name})
            v1_api.register(attr())
urlpatterns.append( re_path(r"^api/", include(v1_api.urls)) )
