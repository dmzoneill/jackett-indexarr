# -*- coding: utf-8 -*-
from setuptools import setup

packages = ["jackett_indexarr"]

package_data = {"": ["*"]}

install_requires = ["requests", "typer"]

entry_points = {"console_scripts": ["jackett-indexarr = jackett_indexarr.cli:app"]}

setup_kwargs = {
    "name": "jackett-indexarr",
    "version": "0.16.5",
    "description": "",
    "long_description": "# Python app to configure sonarr, lidarr & radarr with jackett configured trackers\n\n## Install\n```console\npip install jackett-indexarr\njackett-indexarr```\n\n## How to use\n\n## Support\nFeel free to submit a pull request",
    "author": "David O Neill",
    "author_email": "dmz.oneill@gmail.com",
    "maintainer": None,
    "maintainer_email": None,
    "url": "https://github.com/dmzoneill/jackett-indexarr",
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "entry_points": entry_points,
    "python_requires": ">=3.8,<4.0",
}


setup(**setup_kwargs)
