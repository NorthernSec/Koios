from django.apps import AppConfig


class KoiosAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'koios_admin'
    applet_meta = {
        "url_slug": "/"
    }
