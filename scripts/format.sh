#!/bin/sh -e

isort main.py
isort app/

black main.py
black app/