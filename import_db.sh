#!/usr/bin/env bash

FIXTURE_DIR="postapp/fixtures"

if [ -n "$1" ]; then
  FIXTURE="$FIXTURE_DIR/$1"
else
  candidates=$(find "$FIXTURE_DIR" -type f -name 'postapp_*.json' -printf "%T@ %p\n" 2>/dev/null)
  sorted=$(echo "$candidates" | sort -nr)
  latest_line=$(echo "$sorted" | head -n 1)
  FIXTURE=$(echo "$latest_line" | cut -d' ' -f2-)
fi

if [ ! -f "$FIXTURE" ]; then
  echo "Fixture not found: $FIXTURE"
  exit 1
fi

echo "Running migrations..."
python3 manage.py migrate

echo "Loading data from $FIXTURE..."
python3 manage.py loaddata "$FIXTURE"
echo "Restore complete"
