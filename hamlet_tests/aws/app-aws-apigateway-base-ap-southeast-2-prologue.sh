#!/usr/bin/env bash
#--Hamlet-RequestReference=
#--Hamlet-ConfigurationReference=
#--Hamlet-RunId=027xqsfhdh
clear_bucket_files=()
case ${STACK_OPERATION} in
  delete)
    deleteTreeFromBucket "ap-southeast-2" "##MockOutputXs3XappXapigatewaybaseXdocsXnameX##" "" || return $?
    ;;
  create|update)
    debug "FILES=${clear_bucket_files[@]}"
    #
    syncFilesToBucket "ap-southeast-2" "##MockOutputXs3XappXapigatewaybaseXdocsXnameX##" "" "clear_bucket_files" --delete || return $?
    ;;
 esac
#
deleteBucket ap-southeast-2 ##MockOutputXs3XappXapigatewaybaseXdocsXnameX## || return $?
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
    syncFilesToBucket "ap-southeast-2" "##MockOutputXs3XsegmentXoperationsX##" "settings/mockedup/integration/application/apigatewaybase/config" "configFiles"  || return $?
    ;;
 esac
#
