#!/bin/bash
set -euo pipefail

# Create Schemas
echo "-- schemas"

schema_dir="${TEST_SCHEMA_DIR:-"$(pwd)/.schemas/"}"
[[ -d "${schema_dir}" ]] && rm -r  "${schema_dir}"

hamlet -i mock -p shared -p aws -p azure -p diagrams schema create-schemas -o "${schema_dir}"
