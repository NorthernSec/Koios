import logging
import tomllib
from pathlib import Path

logger = logging.getLogger("koios")

for file in list(Path('.').rglob('applet.toml')):
    try:
        with open(file, 'rb') as f:
            data = tomllib.load(f)
        folder = data.get('project', {}).get('folder')
        if folder:
            applet_folder = Path(file).parent
            if str(applet_folder) != folder:
                applet_folder.rename(folder)
                logger.warning(f"Applet folder {applet_folder} renamed to {folder} as per applet.toml")
    except:
        pass
