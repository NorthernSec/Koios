# Applet creation
A Koios applet is a Django app placed under `app/`. Koios discovers applets by scanning for an `apps.py` file with an `AppConfig` class that defines `applet_meta`. Applets can provide views, URLs, models, templates, and Tastypie API resources.

## File Layout
```text
app/
 |- my_applet/
     |- __init__.py
     |- admin.py     # optional
     |- api.py       # optional, for Tastypie API resources
     |- applet.toml
     |- apps.py
     |- models.py    # optional
     |- static/      # optional
     |- templates/   # optional
     |- tests.py     # optional
     |- urls.py      # optional, for UI/view routes
     |- views.py     # optional
```
### File explanation

| File | Usage |
|---|---|
| **admin.py** | File to set custom rules for data in the `/admin/` url. |
| **applet.toml** | `toml` file containing applet info. |
| **apps.py** | Most important file for applet containing variables & imports. |
| **models.py** | This file contains database structures for your applet. |
| **static/** | Folder containing custom static files (JavaScript, CSS, fonts, ...) |
| **templates/** | Folder for your `html` templates. |
| **tests.py** | File for unit tests. |
| **urls.py** | Custom URL endpoints for this applet. |
| **views.py**| Handles the code for the custom endpoints. |

### Getting started
Koios integrates a modified version of Django's `startapp`. This is part of the integrated **koios_admin** applet, and is also made available through the `Makefile`.
You can create your project template by running:
```bash
make startapp name=applet_name
```

### Custom Koios Applet Files
#### apps.py
Every applet needs a compliant `apps.py` file, with a valid `AppConfig` and valid `applet_meta`.
```python
from django.apps import AppConfig

class MyAppletConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "my_applet"

    applet_meta = {
        "url_slug": "my-applet",
        "nav": {
            "name": "My Applet",
            "icon": "box",
            "endpoint": "my_applet:index",
        },
        "dependencies": {
            "apps": [],
            "middleware": [],
            "template_context_processors": [],
            "template_libraries": {},
            "authentication_backends": [],
            "extra_vars": {},
        },
    }
```
`url_slug` is used to give your applet a unique section in Koios. This will be used to set the root of your applet. In this example, your applet would be hosted under: `https://my.koios.instance/my-applet/`

`nav` contains the application structure you want to put on Koios. This will allow your users to help navigate your applet. Read more [here](docs/applets/metadata_-_nav.md)

`dependencies` contains the dependencies that would normally be loaded in the `settings.py` file of a Django project. `extra_vars` is used to set variables directly to the `settings.py` file.

#### applet.toml
```toml
[project]
name = "My Applet"
description = "Simple description of my applet"
version = "0.1.0"
authors = [
    "Your name and info"
]

[python]
dependencies = [
    "requests"
]

[apt]
packages = [
    "libpango-1.0-0"
]
```

The `project` section is free-form, and is to provide the users of your applet with additional information.

The `python` section has the `dependencies` variable, which can contain a list of python dependencies your project relies on. These should be installable through `pip`.

`apt` contains the variable `packages`, which is a list containing packages that should be installed through `apt`.
**NOTE:** This is the only part of Koios that requires re-building of the docker container if this changes. This to limit the potential splash-area of a compromised applet.

#### urls.py
```python
from django.urls import path
from my_applet   import views

app_name = 'my-applet'

urlpatterns = [
    path('',         views.index,    name='index'),
    path('index',    views.index,    name='index'),
    path('settings', views.settings, name='settings'),
]
```

In the above example, there are a couple of subtle yet important notes.
`app_name` is an important variable that is used during reverse page look-ups. When set, you can refer to your pages like: `my-applet:index`, both in your code, and in your templates.

Sometimes, setting an `app_name` may not work, for example when extending an existing applet. In this case, naming your paths becomes very important.
When `app_name` is not set, the previous example would become `index`, which may conflict with other applets. In this case, it is very important to name your paths in a more unique way, like `my_applet_index`.

The final URL will include the `url_slug` from the `apps.py` file, and thus will become: `/url_slug/path`, or in this case: `/my-applet/index`.

You may have noticed that we have two entries for `index` in this example. In our example, both `/my-applet/` and `/my-applet/index` will route to the function `views.index`.

#### api.py
This section still needs to be documented, as this may change in the near future. Once confirmed, this will be documented.

#### Other files
The other files behave like standard Django app files. You can read the [Django documentation](https://docs.djangoproject.com/en/6.0/intro/tutorial01/) for more information.