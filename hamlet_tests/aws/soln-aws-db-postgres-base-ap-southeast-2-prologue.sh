#!/usr/bin/env bash
#--Hamlet-RequestReference=SRVREQ01
#--Hamlet-ConfigurationReference=configRef_v123
#--Hamlet-RunId=runId098
case ${STACK_OPERATION} in
  create|update)
# Check Snapshot MasterUserName
check_rds_snapshot_username "ap-southeast-2"  "##MockOutputXmanualsnapshotXrdsXdbXpostgresdbbaseXnameX##"  "testUser" || return $?
# Create RDS snapshot
function create_deploy_snapshot() {
info "Creating Pre-Deployment snapshot... "
create_snapshot "ap-southeast-2"  "instance"  "mockedup-integration-database-postgresdbbase"  "mockedup-integration-database-postgresdbbase-890dInur-pre-deploy" || return $?
create_pseudo_stack "RDS Pre-Deploy Snapshot" "${CF_DIR}/$(fileBase "${BASH_SOURCE}")-pseudo-stack.json" "snapshotXrdsXdbXpostgresdbbaseXname" "mockedup-integration-database-postgresdbbase-890dInur-pre-deploy" "manualsnapshotXrdsXdbXpostgresdbbaseXname" "" "Account" "0123456789" "Region" "ap-southeast-2" "DeploymentUnit" "aws-db-postgres-base-prologue" "DeploymentMode" "update"  || return $?
}
create_deploy_snapshot || return $?
 ;;
 esac
