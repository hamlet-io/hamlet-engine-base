#!/bin/bash
set -euo pipefail

engine="${1:-"unicycle"}"
test_script="${2:-""}"

echo "[%] Setting up engine"

script_dir="$( cd "$(dirname "${BASH_SOURCE[0]}")"; pwd )"

tests_dir="${script_dir}/tests"

export HAMLET_HOME_DIR="${script_dir}/.hamlet_home"
[[ -d "${HAMLET_HOME_DIR}" ]] && rm -r "${HAMLET_HOME_DIR}"
mkdir -p "${HAMLET_HOME_DIR}"

hamlet engine install-engine "${engine}"

echo "[%] Environment setup"

eval "$(hamlet --engine "${engine}" engine env)"
env | egrep "(GENERATION|AUTOMATION).*" | sort

echo "[%] Running testing"

for f in ${tests_dir}/test_*.sh; do
  pushd "$(pwd)" > /dev/null
  if [[ -n "${test_script}" ]]; then
    if [[ "${f}" == *"${test_script}"* ]]; then
        echo "Running test script: ${f}"
        . "$f" || exit $?
    fi
  else
    echo ""
    echo "[%] Running test script: ${f}"
    echo ""
    . "$f" || exit $?
  fi
  popd > /dev/null
done

echo "[%] Tests complete!"
