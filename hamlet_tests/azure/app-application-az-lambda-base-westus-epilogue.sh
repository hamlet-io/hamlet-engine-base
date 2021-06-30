#!/usr/bin/env bash
#--Hamlet-RequestReference=SRVREQ01
#--Hamlet-ConfigurationReference=configRef_v123
#--Hamlet-RunId=runId098
az_copy_from_blob "mgmtbaselinesubscription" "" "mockedup/application-az-lambda-base/123456789#MockCommit#/.zip" "${tmpdir}/.zip" "/subscriptions/0123456789/resourceGroups/mockRG/providers/Microsoft.Mock/mockResourceType/mockName" || return $?
#
addToArray functionFiles "${tmpdir}/.zip"
#
    info "${DEPLOYMENT_OPERATION} Function App ... "
    az_functionapp_deploy "/subscriptions/0123456789/resourceGroups/mockRG/providers/Microsoft.Mock/mockResourceType/mockName" ${RESOURCE_GROUP} "mockedup-int-app-lambda-api-/subscriptions/0123456789/resourceGroups/mockRG/providers/Microsoft.Mock/mockResourceType/mockName" "${functionFiles[0]}" ${DEPLOYMENT_OPERATION} || return $?
