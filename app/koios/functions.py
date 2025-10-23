import inspect
import os
import json
from types               import SimpleNamespace
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http       import HttpForbidden
from koios.config        import Config


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


def get_module_calling():
    """Find which module called the function.
       The function ignores this module, so it can be re-used in functions."""
    frame  = inspect.currentframe()
    while True:
        frame  = frame.f_back
        module = inspect.getmodule(frame)
        if module.__name__ != "koios.functions":
            break
    folder = module.__name__.split(".")[0]
    return folder


# Data functions
def get_file_path(filename):
    basedir = Config().data_path
    app     = get_module_calling()
    file    = basedir / app / filename
    return file


def write_to_data(filename, data):
    file = get_file_path(filename)
    # Write data
    file.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, str):
        data = data.encode('utf-8')
    with open(file, 'wb') as f:
        f.write(data)


def read_from_data(filename):
    file = get_file_path(filename)
    if not file.is_file():
        return None
    with open(file, 'rb') as f:
        data = f.read()
        try:
            data = data.decode("utf-8")
        except:
            pass
        return data


data = SimpleNamespace(write=write_to_data, read=read_from_data, filepath=get_file_path)
