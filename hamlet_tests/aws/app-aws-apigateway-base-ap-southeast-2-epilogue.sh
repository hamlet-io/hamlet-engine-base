#!/usr/bin/env bash
#--Hamlet-RequestReference=SRVREQ01
#--Hamlet-ConfigurationReference=configRef_v123
#--Hamlet-RunId=runId098
tmp_filename="openapi_runId098.json"
if [[ -f "${CONFIG}" ]]; then
  cp "${CONFIG}" "${tmpdir}/${tmp_filename}" || return $?
  addToArray configFiles "${tmpdir}/${tmp_filename}"
fi
case ${STACK_OPERATION} in
  delete)
    deleteTreeFromBucket "ap-southeast-2" "##MockOutputXs3XsegmentXoperationsX##" "settings/mockedup/integration/application/apigatewaybase/config" || return $?
    ;;
  create|update)
    debug "FILES=${configFiles[@]}"
    #
    syncFilesToBucket "ap-southeast-2" "##MockOutputXs3XsegmentXoperationsX##" "settings/mockedup/integration/application/apigatewaybase/config" "configFiles" --delete || return $?
    ;;
 esac
#
