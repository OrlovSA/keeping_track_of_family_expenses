#!/bin/sh -e

flake8 main.py
flake8 app/

black main.py --check
black app/ --check