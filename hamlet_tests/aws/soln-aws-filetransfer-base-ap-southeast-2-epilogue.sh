#!/usr/bin/env bash
#--Hamlet-RequestReference=SRVREQ01
#--Hamlet-ConfigurationReference=configRef_v123
#--Hamlet-RunId=runId098
case ${STACK_OPERATION} in
  create|update)
    info "Assigning security group to transfer vpc endpoint..."
    manage_transfer_security_groups     "ap-southeast-2"      "${STACK_OPERATION}"      "${STACK_NAME}"      "securityGroupXtransferServerXappXfiletransferbase"      "transferServerXappXfiletransferbase" || return $?
     ;;
esac
