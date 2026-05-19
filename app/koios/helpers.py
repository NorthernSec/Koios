import json
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions         import PermissionDenied
from django.db.models               import Q
from tastypie.exceptions            import ImmediateHttpResponse
from tastypie.http                  import HttpForbidden

#####
# Decorators

def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if u.groups.filter(
                Q(name__in=group_names) |
                Q(name__in=[f"oidc:{name}" for name in group_names])
            ).exists() or u.is_superuser:
                return True
        raise PermissionDenied
    return user_passes_test(in_groups)

#####
# Immediate Responses
def raise_forbidden(data):
    raise ImmediateHttpResponse(
        HttpForbidden(json.dumps( { "error": True, "message": data } ),
                      content_type='application/json') )
