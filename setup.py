# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jackett_indexerarr']

package_data = \
{'': ['*']}

install_requires = \
['requests', 'typer']

entry_points = \
{'console_scripts': ['jackett-indexerarr = jackett_indexerarr.cli:app']}

setup_kwargs = {
    'name': 'jackett-indexerarr',
    'version': '0.15',
    'description': '',
    'long_description': '# Python app to configure sonarr, lidarr & radarr with jackett configured trackers\n\n## Install\n```console\npip install jackett-indexerarr\n```\n\n## How to use\n```console\njackett-indexerarr ```yaml\nstages:\n  - publish\n\nproduction:\n  image: python:3.8.3-buster\n  stage: publish\n  script:\n    - pip install jackett-indexerarr\n    - jacket-indexerarr\n```\n\n## Support\nFeel free to submit a pull request',
    'author': 'David O Neill',
    'author_email': 'dmz.oneill@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dmzoneill/jackett-indexerarr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
