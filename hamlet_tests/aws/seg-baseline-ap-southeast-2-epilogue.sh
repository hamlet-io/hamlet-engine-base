#!/usr/bin/env bash
#--Hamlet-RequestReference=SRVREQ01
#--Hamlet-ConfigurationReference=configRef_v123
#--Hamlet-RunId=runId098
function manage_ssh_credentials() {
  info "Checking SSH credentials ..."
  #
  # Create SSH credential for the segment
  mkdir -p "${SEGMENT_OPERATIONS_DIR}"
  create_pki_credentials "${SEGMENT_OPERATIONS_DIR}" "ap-southeast-2" "mockacct" ".aws-mockacct-ap-southeast-2-ssh-crt.pem" ".aws-mockacct-ap-southeast-2-ssh-prv.pem" || return $?
  #
  # Update the credential if required
  if ! check_ssh_credentials "ap-southeast-2" "${key_pair_name}"; then
    pem_file="${SEGMENT_OPERATIONS_DIR}/.aws-mockacct-ap-southeast-2-ssh-crt.pem"
    update_ssh_credentials "ap-southeast-2" "${key_pair_name}" "${pem_file}" || return $?
    [[ -f "${SEGMENT_OPERATIONS_DIR}/.aws-mockacct-ap-southeast-2-ssh-prv.pem.plaintext" ]] && 
      { encrypt_kms_file "ap-southeast-2" "${SEGMENT_OPERATIONS_DIR}/.aws-mockacct-ap-southeast-2-ssh-prv.pem.plaintext" "${SEGMENT_OPERATIONS_DIR}/.aws-mockacct-ap-southeast-2-ssh-prv.pem" "alias/mockedup-integration" || return $?; }
  fi
  #
create_pseudo_stack "SSH Key Pair" "${CF_DIR}/$(fileBase "${BASH_SOURCE}")-keypair-pseudo-stack.json" "keypairXsegment" "${key_pair_name}" "keypairXsegmentXname" "${key_pair_name}" "Account" "0123456789" "Region" "ap-southeast-2" "DeploymentUnit" "baseline-epilogue" "DeploymentMode" "update"  || return $?
   info "Removing old ssh pseudo stack output ..."
   legacy_pseudo_stack_file="$(fileBase "${BASH_SOURCE}")"
   legacy_pseudo_stack_filepath="${CF_DIR/baseline/cmk}/${legacy_pseudo_stack_file/-baseline-/-cmk-}-keypair-pseudo-stack.json"
   if [ -f "${legacy_pseudo_stack_filepath}" ]; then
       info "Deleting ${legacy_pseudo_stack_filepath} ..."
       rm -f "${legacy_pseudo_stack_filepath}"
   else
       warn "Unable to locate pseudo stack file ${legacy_pseudo_stack_filepath}"
   fi
  #
  show_ssh_credentials "ap-southeast-2" "${key_pair_name}"
  #
  return 0
}
#
# Determine the required key pair name
key_pair_name="mockedup-integration"
#
case ${STACK_OPERATION} in
  delete)
    delete_ssh_credentials  "ap-southeast-2" "${key_pair_name}" || return $?
    delete_pki_credentials "${SEGMENT_OPERATIONS_DIR}" || return $?
    rm -f "${CF_DIR}/$(fileBase "${BASH_SOURCE}")-keypair-pseudo-stack.json"
    ;;
  create|update)
    manage_ssh_credentials || return $?
    ;;
 esac
case ${STACK_OPERATION} in
  delete)
    delete_oai_credentials "ap-southeast-2" "mockedup-integration" || return $?
    rm -f "${CF_DIR}/$(fileBase "${BASH_SOURCE}")-pseudo-stack.json"
    ;;
  create|update)
    info "Removing legacy oai credential ..."
    used=$(is_oai_credential_used "ap-southeast-2" "mockedup-integration" ) || return $?
    if [[ "${used}" == "true" ]]; then
      warn "Legacy OAI in use - rerun the baseline unit to remove it once it is no longer in use ..."
    else
      delete_oai_credentials "ap-southeast-2" "mockedup-integration" || return $?
      info "Removing legacy oai pseudo stack output"
      legacy_pseudo_stack_file="$(fileBase "${BASH_SOURCE}")"
      legacy_pseudo_stack_filepath="${CF_DIR/baseline/cmk}/${legacy_pseudo_stack_file/-baseline-/-cmk-}-pseudo-stack.json"
      if [ -f "${legacy_pseudo_stack_filepath}" ]; then
         info "Deleting ${legacy_pseudo_stack_filepath} ..."
         rm -f "${legacy_pseudo_stack_filepath}"
      else
         warn "Unable to locate pseudo stack file ${legacy_pseudo_stack_filepath}"
      fi
    fi
    ;;
 esac
