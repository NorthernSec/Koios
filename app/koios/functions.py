import os
import json
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http       import HttpForbidden


runpath = os.path.dirname(os.path.realpath(__file__))

def get_projects():
    projects = []
    for path, folders, files in os.walk(os.path.join(runpath, "..")):
        if "models.py" in files:
            projects.append(os.path.basename(path))
    return projects


def raise_forbidden(data):
    raise ImmediateHttpResponse(
        HttpForbidden(json.dumps( { "error": True, "message": data } ),
                      content_type='application/json') )
