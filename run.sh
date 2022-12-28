#!/bin/bash

set -e

exec python app.py &
exec python main.py 