#!/usr/bin/env bash
#--Hamlet-RequestReference=
#--Hamlet-ConfigurationReference=
#--Hamlet-RunId=iyrffg8wte
tmp_filename="config.json"
if [[ -f "${CONFIG}" ]]; then
  cp "${CONFIG}" "${tmpdir}/${tmp_filename}" || return $?
  addToArray configFiles "${tmpdir}/${tmp_filename}"
fi
case ${STACK_OPERATION} in
  delete)
    deleteTreeFromBucket "ap-southeast-2" "##MockOutputXs3XsegmentXoperationsX##" "settings/mockedup/integration/application/mobileappbase/config" || return $?
    ;;
  create|update)
    debug "FILES=${configFiles[@]}"
    #
    syncFilesToBucket "ap-southeast-2" "##MockOutputXs3XsegmentXoperationsX##" "settings/mockedup/integration/application/mobileappbase/config" "configFiles" --delete || return $?
    ;;
 esac
#
