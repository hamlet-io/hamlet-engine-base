#!/usr/bin/env bash
#--Hamlet-RequestReference=SRVREQ01
#--Hamlet-ConfigurationReference=configRef_v123
#--Hamlet-RunId=runId098
copyFilesFromBucket ap-southeast-2 account-registry-abc123 pipeline/mockedup/aws-datapipeline-base/123456789#MockCommit# "${tmpdir}" || return $?
#
addToArray pipelineFiles "${tmpdir}/pipeline.zip"
#
case ${STACK_OPERATION} in
  delete)
    deleteTreeFromBucket "ap-southeast-2" "##MockOutputXs3XsegmentXoperationsX##" "settings/mockedup/integration/application/datapipelinebase/pipeline" || return $?
    ;;
  create|update)
    debug "FILES=${pipelineFiles[@]}"
    #
    syncFilesToBucket "ap-southeast-2" "##MockOutputXs3XsegmentXoperationsX##" "settings/mockedup/integration/application/datapipelinebase/pipeline" "pipelineFiles" --delete || return $?
    ;;
 esac
#
tmp_filename="config.json"
if [[ -f "${CONFIG}" ]]; then
  cp "${CONFIG}" "${tmpdir}/${tmp_filename}" || return $?
  addToArray configFiles "${tmpdir}/${tmp_filename}"
fi
case "${STACK_OPERATION}" in
  create|update)
       mkdir "${tmpdir}/pipeline"
       unzip "${tmpdir}/pipeline.zip" -d "${tmpdir}/pipeline"
       # Get cli config file
       split_cli_file "${CLI}" "${tmpdir}" || return $?
       # Create Data pipeline
       info "Applying cli level configurtion"
       pipelineId="$(create_data_pipeline       "ap-southeast-2"        "${tmpdir}/cli-datapipelineXappXdatapipelinebase-createPipeline.json")"
       # Add Pipeline Definition
       info "Updating pipeline definition"
       update_data_pipeline       "ap-southeast-2"        "${pipelineId}"        "${tmpdir}/pipeline/pipeline-definition.json"        "${tmpdir}/pipeline/pipeline-parameters.json"        "${tmpdir}/config.json"        "${STACK_NAME}"        "securityGroupXappXdatapipelinebase" || return $?
create_pseudo_stack "Data Pipeline" "${CF_DIR}/$(fileBase "${BASH_SOURCE}")-creds-system-pseudo-stack.json" "datapipelineXappXdatapipelinebase" "${pipelineId}" "Account" "0123456789" "Region" "ap-southeast-2" "DeploymentUnit" "aws-datapipeline-base-epilogue" "DeploymentMode" "update"  || return $?
   ;;
   esac
