#!/usr/bin/env bash

OUTDIR="postapp/fixtures"
TIMESTAMP=$(date +"%Y-%m-%dT%H-%M-%S")
OUTFILE="$OUTDIR/postapp_${TIMESTAMP}.json"

mkdir -p "$OUTDIR"

echo "Dumping postapp data to $OUTFILE..."
python3 manage.py dumpdata postapp.PostTag postapp.Post --indent 2 >"$OUTFILE"
echo "Backup complete"
