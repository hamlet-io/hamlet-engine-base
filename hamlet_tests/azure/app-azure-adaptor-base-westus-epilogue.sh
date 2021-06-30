#!/usr/bin/env bash
#--Hamlet-RequestReference=SRVREQ01
#--Hamlet-ConfigurationReference=configRef_v123
#--Hamlet-RunId=runId098
az_copy_from_blob "mgmtbaselinesubscription" "" "mockedup/azure-adaptor-base/123456789#MockCommit#/.zip" "${tmpdir}/.zip" "" || return $?
#
addToArray src_zip "${tmpdir}/.zip"
#
addToArray src "${tmpdir}/src/"
unzip "${src_zip}" -d "${src}"
tmp_filename="$(fileName "${CONFIG}")"
if [[ -f "${CONFIG}" ]]; then
  cp "${CONFIG}" "${tmpdir}/${tmp_filename}" || return $?
  addToArray config "${tmpdir}/${tmp_filename}"
fi
