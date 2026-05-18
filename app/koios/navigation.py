from django.apps import apps

def build_nav():
    """
    Collects nav from all installed apps into a single structure.
    Each app contributes its own section; order is preserved.
    """
    menu = []

    for config in apps.get_app_configs():
        app_meta = getattr(config, "applet_meta", {})
        if app_meta and app_meta.get('nav'):
            item = {"app_name": config.name}
            item.update(app_meta['nav'])
            menu.append(item)
    menu = sorted(menu, key=lambda x: x['app_name'])
    return menu

# Build once at startup
NAVIGATION = build_nav()
