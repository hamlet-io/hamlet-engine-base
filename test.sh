#!/bin/bash
set -euo pipefail

engine="${1}"
test_script="${2:-""}"

echo "[%] Setting up engine"

script_dir="$( cd "$(dirname "${BASH_SOURCE[0]}")"; pwd )"

tests_dir="${script_dir}/tests"

export HAMLET_ENGINE="${engine}"
export HAMLET_ENGINE_DIR="${script_dir}/.hamlet_home"
export HAMLET_ENGINE_CONFIG="${script_dir}"

[[ -d "${HAMLET_ENGINE_DIR}" ]] && rm -r "${HAMLET_ENGINE_DIR}"
mkdir -p "${HAMLET_ENGINE_DIR}"

hamlet engine install-engine

echo "[%] Environment setup"

eval "$(hamlet engine env)"
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
