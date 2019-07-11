# -*- coding: utf-8 -*-
from distutils.core import setup

packages = ["add_ticket_hook"]

package_data = {"": ["*"]}

setup_kwargs = {
    "name": "add-ticket-hook",
    "version": "0.1.0",
    "description": "Add ticket number to your git commit message.",
    "long_description": None,
    "author": "Antti Ruotsalainen",
    "author_email": "antti.ruotsalainen@vuoma.fi",
    "url": None,
    "packages": packages,
    "package_data": package_data,
    "python_requires": ">=3.7,<4.0",
}


setup(**setup_kwargs)
