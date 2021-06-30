#!/usr/bin/env bash
#--Hamlet-RequestReference=SRVREQ01
#--Hamlet-ConfigurationReference=configRef_v123
#--Hamlet-RunId=runId098
case ${DEPLOYMENT_OPERATION} in
  create|update)
    ADMINGRP=$(az role definition list --name 1234567890-1234567890-1234567890-1234567890)
    if [[ ${#ADMINGRP[@]} -eq 0 ]] ; then
      fatal "Azure Administrator role does not exist: 1234567890-1234567890-1234567890-1234567890"
      return 1
    fi
create_pseudo_stack "AdministratorGroups" "${CF_DIR}/$(fileBase "${BASH_SOURCE}")-admingrp-pseudo-stack.json" "vaultXmgmtXbaselineX1234567890X1234567890X1234567890X1234567890" "1234567890-1234567890-1234567890-1234567890" "Subscription" "0123456789" "ResourceGroup" "mockedup-integration-default-seg-baseline" "Region" "westus" "DeploymentUnit" "baseline" "DeploymentMode" "update"  || return $?
       ;;
       esac
