#!/usr/bin/env bash
#--Hamlet-RequestReference=SRVREQ01
#--Hamlet-ConfigurationReference=configRef_v123
#--Hamlet-RunId=runId098
if [[ ! ${DEPLOYMENT_OPERATION} == delete ]]; then
    CONNECTION_STRING=$(az_get_storage_connection_string "appspasubscriptions01234")
   az storage blob service-properties update --connection-string "${CONNECTION_STRING}" --static-website true
fi
case ${DEPLOYMENT_OPERATION} in
  delete)
    az_delete_blob_dir "appspasubscriptions01234" "settings/mockedup/integration/application/spa/spa" || return $?
    ;;
  create|update)
    debug "FILES=${spaFiles[@]}"
    #
    az_sync_with_blob "appspasubscriptions01234" "\$web" "settings/mockedup/integration/application/spa/spa" "spaFiles" || return $?
    ;;
 esac
#
case ${DEPLOYMENT_OPERATION} in
  delete)
    az_delete_blob_dir "appspasubscriptions01234" "settings/mockedup/integration/application/spa/config" || return $?
    ;;
  create|update)
    debug "FILES=${configFiles[@]}"
    #
    az_sync_with_blob "appspasubscriptions01234" "\$web" "settings/mockedup/integration/application/spa/config" "configFiles" || return $?
    ;;
 esac
#
