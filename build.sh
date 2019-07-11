#!/bin/bash

#
# Generates a new setup.py file

# start clean up
rm -rf dist

# generate a new file
poetry build
tar -xzvf dist/*tar.gz
cp add_ticket_hook-*/setup.py .

# end clean up
rm -rf add_ticket_hook-*
rm -rf dist
