#!/usr/bin/env bash
#--Hamlet-RequestReference=SRVREQ01
#--Hamlet-ConfigurationReference=configRef_v123
#--Hamlet-RunId=runId098
az_copy_from_blob "mgmtbaselinesubscription" "" "mockedup/application-az-spa-base/123456789#MockCommit#/.zip" "${tmpdir}/.zip" "" || return $?
#
addToArray spaFiles "${tmpdir}/.zip"
#
tmp_filename="config.json"
if [[ -f "${CONFIG}" ]]; then
  cp "${CONFIG}" "${tmpdir}/${tmp_filename}" || return $?
  addToArray configFiles "${tmpdir}/${tmp_filename}"
fi
