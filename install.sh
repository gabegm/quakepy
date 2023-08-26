#!/bin/bash

mkdir ~/.venvs
python3 -m venv ~/.venvs/quakepy
source ~/.venv/quakepy/bin/activate
pip3 install -r requirements.txt