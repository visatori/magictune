#!/bin/bash

cd /app
python magictune.py --dry-run=$DRY_RUN --hide-low-volume=$HIDE_LOW_VOLUME run > /proc/1/fd/1 2>/proc/1/fd/2