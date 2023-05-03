#!/usr/bin/env bash
# -*- coding: utf-8 -*-
intro="""
Ths entrypoint script @ $(pwd) is used to start the server in the container.
It can be used to provide custom configuration options during server startup.
It can also be used to run tests, linting, etc. before starting the server.
"""
echo "$intro"

cd /app
#python3 /app/src/main.py --app "main:app" --proxy-headers "True" --host "0.0.0.0" --port 8000 --reload "True"
python3 -m uvicorn  main:app --proxy-headers  --host "0.0.0.0" --port 8000 --reload \
--use-colors
