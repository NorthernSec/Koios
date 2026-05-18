from django.urls      import reverse, NoReverseMatch
from koios.navigation import NAVIGATION


def has_access(item, user):
    required_perm = item.get("required_perm")
    if required_perm and not user.has_perm(required_perm):
        return False
    return True

def get_endpoint(endpoint):
    try:
        reverse(endpoint)
        return endpoint
    except NoReverseMatch:
        # TODO: Proper logging
        print(f"No reverse match for {filtered_item['endpoint']}")
        return None


def modular_nav(request):
    """
    Exposes the modular navbar to templates.
    Filters out items the user cannot see based on 'required_perm'.
    """
    user = request.user

    filtered_menu = []

    for app in NAVIGATION:
        filtered = filter_nav_item(app, user)
        if filtered:
            filtered_menu.append(filtered)
    return {"modular_nav": filtered_menu}


def filter_nav_item(item, user):
    """
    Recursively filter a nav item and its children based on permissions.
    Returns None if the user does not have access to the item or any children.
    """
    def recursive_filter(i):
        if not has_access(i, user):
            return None
        if i.get('sections'):
            sections = [recursive_filter(s) for s in i['sections']]
            i['sections'] = [s for s in sections if s]
        if i.get('endpoint'):
            i['endpoint'] = get_endpoint( i["endpoint"] )
        return i


    required_perm = item.get("required_perm")
    if required_perm and not user.has_perm(required_perm):
        return None

    filtered_item = recursive_filter(item.copy())
    return filtered_item
