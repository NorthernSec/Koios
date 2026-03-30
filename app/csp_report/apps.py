from django.apps import AppConfig


class CspReportConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name        = 'csp_report'
    applet_meta = {
        "nav_label":    None,
        "nav":          [],
        "url_slug":     "csp-report",
        "dependencies": {
            'apps':         [ 'csp' ],
            "middleware":   [ 'csp.middleware.CSPMiddleware' ],
            "template_context_processors": [ 'csp.context_processors.nonce' ],
            "template_libraries":          { "csp": "csp.templatetags.csp" },

        }
    }
