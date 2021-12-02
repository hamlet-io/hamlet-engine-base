#!/bin/bash
set -euo pipefail

# Create a CMDB
echo "-- cmdb build"

test_cmdb="${TEST_GENERATE_DIR:-"$(pwd)/.generate_cmdb/"}"
[[ -d "${test_cmdb}" ]] && rm -r "${test_cmdb}"

export ROOT_DIR="${test_cmdb}"

tenant="test_ten1"
account="test_acct1"
product="test_product1"
provider_id="1234567890"

environment="integration"
segment="default"

hamlet generate tenant-cmdb -o "${test_cmdb}" --tenant-id "${tenant}"
hamlet generate account-cmdb -o "${test_cmdb}/${tenant}" --account-id "${account}" --provider-id "${provider_id}"
hamlet generate product-cmdb -o "${test_cmdb}"  --product-id "${product}"

cd ${test_cmdb}/${product}/config/solutionsv2/${environment}/${segment}/
hamlet --account "${account}" component list-occurrences
