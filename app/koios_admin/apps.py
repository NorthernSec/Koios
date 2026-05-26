from django.apps import AppConfig
from koios_admin import settings

class KoiosAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'koios_admin'
    applet_meta = {
        "url_slug": "/",
        "dependencies": {
            "apps":         [ ],
            "middleware":   [ ],
            "template_context_processors": [ ],
            "template_libraries":          { },
        }
    }

    if settings.ENABLE_CSP:
        deps = applet_meta['dependencies']
        deps['apps'].append('csp')
        deps['middleware'].append('csp.middleware.CSPMiddleware')
        deps['template_context_processors'].append('csp.context_processors.nonce')
        deps['template_libraries']['csp'] = "csp.templatetags.csp"

