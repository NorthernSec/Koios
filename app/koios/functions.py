import importlib
import inspect
import os
import json
from types               import SimpleNamespace
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http       import HttpForbidden
from koios.config        import Config


runpath = os.path.dirname(os.path.realpath(__file__))

def is_valid_applet(module_name):
    #TODO: Upgrade to logging
    app = get_applet_app(module_name)
    if not app:
        print(f"Error: {module_name} is not a valid applet, or is broken.")
        return False
    meta = app.applet_meta
    if not meta.get("url_slug"):
        print(f"WARN: {module_name} has no URL slug. It's name will be used")
    if (not isinstance(meta.get("dependencies",{}), dict) or
       not isinstance(meta.get("dependencies",{}).get('apps', []), list) or
       not isinstance(meta.get("dependencies",{}).get('middleware', []), list) or
       not isinstance(meta.get("dependencies",{}).get('template_context_processors', []), list) or
       not isinstance(meta.get("dependencies",{}).get('template_libraries', {}), dict) or
       not isinstance(meta.get("dependencies",{}).get('authentication_backends', []), list) or
       not isinstance(meta.get("dependencies",{}).get('extra_vars', {}), dict)):
        print(f"ERROR: {module_name} has an invalid dependency format. Is it outdated?")
        return False
    return True


def get_applet_app(module_name):
    try:
        module = importlib.import_module(f"{module_name}.apps")
    except Exception as e:
        # TODO: Logging
        print(f"Couldn't import {module_name}: {e}")
        return
    is_app = lambda x: isinstance(getattr(module, x), type)
    apps   = [getattr(module, attr) for attr in dir(module) if is_app(attr)]
    apps   = [app for app in apps if "applet_meta" in dir(app)]
    if len(apps) > 1:
        # TODO: Logging
        print("Invalid applet: Multiple app configs not currently supported.")
        return None
    return apps[0] if apps else None


def get_applets(with_deps=False):
    applets = []
    for path, folders, files in os.walk(os.path.join(runpath, "..")):
        if "apps.py" in files:
            module_name = os.path.basename(path)
            if not is_valid_applet(module_name):
                continue
            app = get_applet_app(module_name)
            if not app:
                continue
            if with_deps:
                deps = app.applet_meta.get('dependencies', {}).get('apps', [])
                applets.extend(deps)
            applets.append(module_name)
    return applets


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
