from django.apps import AppConfig


class {name}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name        = '{name}'
    applet_meta = {{
        "url_slug": "{name}",
        "nav": {{ }},
        "dependencies": {{
            "apps": [ ],
            "middleware": [ ],
            "authentication_backends": [ ],
            "template_context_processors": [ ],
            "template_libraries": {{ }},
            "extra_vars": {{ }}
        }}
    }}
