#!/usr/bin/env bash
#--Hamlet-RequestReference=SRVREQ01
#--Hamlet-ConfigurationReference=configRef_v123
#--Hamlet-RunId=runId098
case ${STACK_OPERATION} in
  create|update)
       rds_hostname="$(get_rds_hostname       "ap-southeast-2"        "instance"        "mockedup-integration-database-postgresdbgenerated" || return $?)"
# Reset Master Password
function reset_master_password() {
info "Getting Master Password... "
encrypted_master_password="##MockOutputXrdsXdbXpostgresdbgeneratedXgeneratedpasswordX##"
master_password="$(decrypt_kms_string "ap-southeast-2"  "${encrypted_master_password}" || return $?)"
info "Resetting Master Password... "
set_rds_master_password "ap-southeast-2"  "instance"  "mockedup-integration-database-postgresdbgenerated"  "${master_password}" || return $?
info "Generating URL... "
rds_url="$(get_rds_url "postgres"  "root"  "${master_password}"  "${rds_hostname}"  "5432"  "mockedup" || return $?)"
encrypted_rds_url="$(encrypt_kms_string "ap-southeast-2"  "${rds_url}"  "arn:aws:iam::123456789012:mock/cmkXsegmentXcmkXarn" || return $?)"
create_pseudo_stack "RDS Connection URL" "${CF_DIR}/$(fileBase "${BASH_SOURCE}")-url-pseudo-stack.json" "rdsXdbXpostgresdbgeneratedXurl" "${encrypted_rds_url}" "Account" "0123456789" "Region" "ap-southeast-2" "DeploymentUnit" "aws-db-postgres-generated-epilogue" "DeploymentMode" "update"  || return $?
}
reset_master_password || return $?
       ;;
       esac
