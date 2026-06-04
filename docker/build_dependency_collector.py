import tomllib
from pathlib import Path

deps = set()

for file in Path('.').rglob('applet.toml'):
    try:
        with open(file, 'rb') as f:
            data = tomllib.load(f)
        deps.update(data.get('apt', {}).get('packages', []))
    except:
        pass

print(' '.join(sorted(deps)))
