#!/usr/bin/env bash
#--Hamlet-RequestReference=SRVREQ01
#--Hamlet-ConfigurationReference=configRef_v123
#--Hamlet-RunId=runId098
case ${STACK_OPERATION} in
  create|update)
       rds_hostname="$(get_rds_hostname       "ap-southeast-2"        "instance"        "mockedup-integration-database-postgresdbbase" || return $?)"
       ;;
       esac
