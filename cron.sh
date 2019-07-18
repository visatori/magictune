#!/bin/bash

cd /app
python magictune.py --dry-run=$DRY_RUN run > /proc/1/fd/1 2>/proc/1/fd/2