import os
from shutil import rmtree
from typing import Optional

import typer
from jackett_indexarr.utils import configure

app = typer.Typer()


@app.command()
def update(
    jackett_cookie: Optional[str] = os.environ.get("jackett_cookie", None),
    jackett_endpoint: Optional[str] = os.environ.get("jackett_endpoint", None),
    jackett_api_key: Optional[str] = os.environ.get("jackett_api_key", None),
    sonarr_db: Optional[str] = os.environ.get("sonarr_db", None),
    radarr_db: Optional[str] = os.environ.get("radarr_db", None),
    lidarr_db: Optional[str] = os.environ.get("lidarr_db", None),
    readarr_db: Optional[str] = os.environ.get("readarr_db", None),
):
    if jackett_cookie is None:
        print(
            "You need to define jackett_cookie, which you can get from a browser session\n\n"
        )
        print('  export jackett_cookie=".........."')
        print("  Or")
        print('  --jackett_cookie="............."')
        return

    if jackett_endpoint is None:
        print("You need to define jackett_endpoint\n\n")
        print('  export jackett_endpoint="http://your-jacket:port"')
        print("  Or")
        print('  --jackett_endpoint="http://your-jacket:port"')
        return

    if jackett_api_key is None:
        print("You need to define jackett_api_key\n\n")
        print('  export jackett_api_key="............."')
        print("  Or")
        print('  --jackett_api_key="............."')
        return

    configure(
        jackett_endpoint,
        jackett_api_key,
        jackett_cookie,
        sonarr_db,
        radarr_db,
        lidarr_db,
        readarr_db,
    )
