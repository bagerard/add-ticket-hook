# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="add-ticket",
    version="0.1.0",
    description="Prefix ticket name and number to commit messages.",
    packages=["add_ticket_hook"],
    entry_points={"console_scripts": ["add-ticket = add_ticket_hook.main:main"]},
)
