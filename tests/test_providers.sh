#!/bin/bash
set -euo pipefail

TEST_OUTPUT_DIR="${TEST_OUTPUT_DIR:-"$(pwd)/.provider_tests/"}"
[[ -d "${TEST_OUTPUT_DIR}" ]] && rm -r "${TEST_OUTPUT_DIR}"

# Test Engine and plugins
echo "-- shared provider"
hamlet -i mock -p sharedtest -p shared -f default deploy test-deployments -p '--junitxml=junit.xml' -o "${TEST_OUTPUT_DIR}/shared/"

echo "-- aws provider"
hamlet -i mock -p aws -p awstest -f cf deploy test-deployments -p '--junitxml=junit.xml' -o "${TEST_OUTPUT_DIR}/aws/"

echo "-- azure provider"
hamlet -i mock -p azure -p azuretest -f arm deploy test-deployments -p '--junitxml=junit.xml' -o "${TEST_OUTPUT_DIR}/azure/"
