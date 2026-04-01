#!/usr/bin/env bash

set -euo pipefail

archive_dir="archive"
source_file="grades.csv"
timestamp="$(date +"%Y%m%d-%H%M%S")"
archived_file="grades_${timestamp}.csv"
log_file="organizer.log"

mkdir -p "$archive_dir"

if [[ ! -f "$source_file" ]]; then
  : > "$source_file"
fi

mv "$source_file" "$archive_dir/$archived_file"
: > "$source_file"

printf '%s | %s | %s\n' \
  "$timestamp" \
  "$source_file" \
  "$archive_dir/$archived_file" >> "$log_file"

