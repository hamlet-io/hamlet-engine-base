#!/usr/bin/env bash
#--Hamlet-RequestReference=SRVREQ01
#--Hamlet-ConfigurationReference=configRef_v123
#--Hamlet-RunId=runId098
case ${STACK_OPERATION} in
  create|update)
    info "Saving secret to CMDB"
    secret_arn="$(get_cloudformation_stack_output "ap-southeast-2"  "${STACK_NAME}" secretXappXqueuehostbaseXroot "ref" || return $?)"
    secret_content="$(aws --region "ap-southeast-2" --output text secretsmanager get-secret-value --secret-id "${secret_arn}" --query "SecretString" || return $?)"
    secret_value="$( echo "${secret_content}" | jq -r ".")"
    kms_encrypted_secret="$(encrypt_kms_string "ap-southeast-2"  "${secret_value}"  "arn:aws:iam::123456789012:mock/cmkXsegmentXcmkXarn" || return $?)"
create_pseudo_stack "KMS Encrypted Secret" "${CF_DIR}/$(fileBase "${BASH_SOURCE}")-secretXappXqueuehostbaseXroot-pseudo-stack.json" "secretXappXqueuehostbaseXrootXsecret" "${kms_encrypted_secret}" "Account" "0123456789" "Region" "ap-southeast-2" "DeploymentUnit" "aws-queuehost-base-epilogue" "DeploymentMode" "update"  || return $?
esac
case ${STACK_OPERATION} in
  create|update)
    info "Generating Encrypted Url"
    secret_arn="$(get_cloudformation_stack_output "ap-southeast-2"  "${STACK_NAME}" secretXappXqueuehostbaseXroot "ref" || return $?)"
    amqp_endopoint="$(get_cloudformation_stack_output "ap-southeast-2"  "${STACK_NAME}" mqBrokerXappXqueuehostbase "dns" || return $?)"
    secret_content="$(aws --region "ap-southeast-2" --output text secretsmanager get-secret-value --secret-id "${secret_arn}" --query "SecretString" || return $?)"
    username="root"
    password="$( echo "${secret_content}" | jq -r ".password")"
    url="${amqp_endopoint/"amqps://"/"amqps://${username}:${password}@"}"
    kms_encrypted_url="$(encrypt_kms_string "ap-southeast-2"  "${url}"  "arn:aws:iam::123456789012:mock/cmkXsegmentXcmkXarn" || return $?)"
create_pseudo_stack "KMS Encrypted Url" "${CF_DIR}/$(fileBase "${BASH_SOURCE}")-pseudo-stack.json" "mqBrokerXappXqueuehostbaseXurl" "${kms_encrypted_url}" "Account" "0123456789" "Region" "ap-southeast-2" "DeploymentUnit" "aws-queuehost-base-epilogue" "DeploymentMode" "update"  || return $?
esac
