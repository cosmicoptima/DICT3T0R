#!/bin/bash

while true
do
        git pull --force
        python3 -m pip install -r requirements.txt
        python3 src/main.py
        echo "Restarting in 2..."
        sleep 2
done