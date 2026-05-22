# Applet Metadata - nav

The format of the `nav` metadata is the following:
```python
    applet_meta = {
        ...
        "nav": {
            "name": "Top nav label",
            # Get icons from https://icons.getbootstrap.com/
            "icon": "pen",
            "endpoint": "<app_name>:<path name>",
            "sections": [
                {
                    "name": "item 1",
                    "endpoint": "<app_name>:<path name>"
                },
                {
                    "name": "item 2",
                    "sections": [
                        {
                            "name": "item 3",
                            "endpoint": "<app_name>:<path name>"
                        },
                        {
                            "name": "item 3",
                            "endpoint": "<app_name>:<path name>"
                        },
                    ]
                }
            ]
        }
    }
```
**Note:** Each item should have either an endpoint or sections. If both are set, endpoints get priority.
Sections can only go 2 levels deep.

| Key | Meaning | Optional |
| --- | --- | --- |
| **name** | The name of the nav item | Required |
| **icon** | The bootstrap icon name | Optional |
| **endpoint** | The Django endpoint name for the desired view | Optional * |
| **sections** | Optional sub-items for the nav item (drop-down) | Optional * |
| **required_perm** | Permissions required to display the item in the navbar | Optional |
