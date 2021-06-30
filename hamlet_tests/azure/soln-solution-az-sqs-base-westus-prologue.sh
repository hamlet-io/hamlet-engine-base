#!/usr/bin/env bash
#--Hamlet-RequestReference=SRVREQ01
#--Hamlet-ConfigurationReference=configRef_v123
#--Hamlet-RunId=runId098
case ${DEPLOYMENT_OPERATION} in
  create|update)
    # Create Storage Account Queue
    info "Creating Queue Storage ... "
    az_interact_storage_queue "mgmtbaselinesubscription" "app-sqs-sqs" "create" || return $?
;;
  delete)
    # Deleting Storage Account Queue
    info "Deleting Queue Storage ... "
    az_interact_storage_queue "mgmtbaselinesubscription" "app-sqs-sqs" "delete" || return $?
;;
esac
