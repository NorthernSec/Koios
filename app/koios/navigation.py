from django.apps import apps

def build_nav():
    """
    Collects nav from all installed apps into a single structure.
    Each app contributes its own section; order is preserved.
    """
    menu = []

    for config in apps.get_app_configs():
        app_nav = getattr(config, "nav", None)
        if app_nav:
            menu.append({
                "name":      config.nav_label,
                "app_label": config.label,
                "sections":  app_nav
            })
    menu = sorted(menu, key=lambda x: x['name'])
    return menu

# Build once at startup
NAVIGATION = build_nav()
