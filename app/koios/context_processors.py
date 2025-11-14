from django.urls      import reverse, NoReverseMatch
from koios.navigation import NAVIGATION

def modular_nav(request):
    """
    Exposes the modular navbar to templates.
    Filters out items the user cannot see based on 'required_perm'.
    """
    user = request.user

    filtered_menu = []

    for app in NAVIGATION:
        app_label = app.get('nav_label', app['app_label'])
        sections = []

        for section in app['sections']:
            filtered_section = filter_nav_item(section, user)
            if filtered_section:
                sections.append(filtered_section)

        if sections:
            filtered_menu.append({
                "app_label": app_label,
                "sections": sections
            })

    return {"modular_nav": filtered_menu}


def filter_nav_item(item, user):
    """
    Recursively filter a nav item and its children based on permissions.
    Returns None if the user does not have access to the item or any children.
    """
    required_perm = item.get("required_perm")
    if required_perm and not user.has_perm(required_perm):
        return None

    filtered_item = item.copy()

    if filtered_item.get("endpoint"):
        try:
            reverse(filtered_item["endpoint"])
        except NoReverseMatch:
            print(f"No reverse match for {filtered_item['endpoint']}")
            filtered_item["endpoint"] = None

    if "children" in item:
        children = [
            child for child in (filter_nav_item(c, user) for c in item["children"])
            if child is not None
        ]
        if not children and not item.get("endpoint"):
            return None  # no accessible children and no section endpoint
        filtered_item["children"] = children

    return filtered_item
