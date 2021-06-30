#!/usr/bin/env bash
#--Hamlet-RequestReference=SRVREQ01
#--Hamlet-ConfigurationReference=configRef_v123
#--Hamlet-RunId=runId098
function az_manage_ssh_credentials() {
  info "Checking SSH credentials ..."
  #
  # Create SSH credential for the segment
  mkdir -p "${SEGMENT_OPERATIONS_DIR}"
  az_create_ssh_keypair "${SEGMENT_OPERATIONS_DIR}" "westus" "mockacct" || return $?
  #
  # Upload to keyvault if required.
  AZ_CHK_SECRET=$(az_check_secret "vault-/subscriptions/0123456789/resourceGroups/mockRG/providers/Microsoft.Mock/mockResourceType/mockName" "secret-mgmt-baseline-sshPublicKey")
  if [[ ${AZ_CHK_SECRET}            = "does not have secrets get permission on key vault" ]]; then
    fatal "The deployment user is not a member of the specified keyVault admin group"
    return 1
  fi
  if [[ ${AZ_CHK_SECRET}          = *NotFound* ]]; then
     pem_file="${SEGMENT_OPERATIONS_DIR}/.azure-mockacct-westus-ssh.plaintext.pub"
     az_add_secret "vault-/subscriptions/0123456789/resourceGroups/mockRG/providers/Microsoft.Mock/mockResourceType/mockName" "secret-mgmt-baseline-sshPublicKey" "${pem_file}"
  fi
  AZ_CHK_SECRET=$(az_check_secret "vault-/subscriptions/0123456789/resourceGroups/mockRG/providers/Microsoft.Mock/mockResourceType/mockName" "secret-mgmt-baseline-sshPrivateKey")
  if [[ ${AZ_CHK_SECRET}          = *NotFound* ]]; then
     pem_file="${SEGMENT_OPERATIONS_DIR}/.azure-mockacct-westus-ssh.plaintext"
     az_add_secret "vault-/subscriptions/0123456789/resourceGroups/mockRG/providers/Microsoft.Mock/mockResourceType/mockName" "secret-mgmt-baseline-sshPrivateKey" "${pem_file}"
  fi
  #
create_pseudo_stack "SSH Key Pair" "${CF_DIR}/$(fileBase "${BASH_SOURCE}")-keypair-pseudo-stack.json" "secretXssh" "secret-mgmt-baseline-ssh" "vaultXXsubscriptionsX0123456789XresourceGroupsXmockRGXprovidersXMicrosoft.MockXmockResourceTypeXmockNameXName" "vault-/subscriptions/0123456789/resourceGroups/mockRG/providers/Microsoft.Mock/mockResourceType/mockName" "Subscription" "0123456789" "ResourceGroup" "mockedup-integration-default-seg-baseline" "Region" "westus" "DeploymentUnit" "baseline" "DeploymentMode" "update"  || return $?
 return 0
}
#
case ${DEPLOYMENT_OPERATION} in
  delete)
  AZ_CHK_SECRET=$(az_check_secret "vault-/subscriptions/0123456789/resourceGroups/mockRG/providers/Microsoft.Mock/mockResourceType/mockName" "secret-mgmt-baseline-sshPublicKey")
  if [[ ! $(${AZ_CHK_SECRET} = *NotFound* ) ]]; then
    az_delete_secret "vault-/subscriptions/0123456789/resourceGroups/mockRG/providers/Microsoft.Mock/mockResourceType/mockName" "secret-mgmt-baseline-sshPublicKey"
  fi
  AZ_CHK_SECRET=$(az_check_secret "vault-/subscriptions/0123456789/resourceGroups/mockRG/providers/Microsoft.Mock/mockResourceType/mockName" "secret-mgmt-baseline-sshPrivateKey")
  if [[ ! $(${AZ_CHK_SECRET} = *NotFound* ) ]]; then
    az_delete_secret "vault-/subscriptions/0123456789/resourceGroups/mockRG/providers/Microsoft.Mock/mockResourceType/mockName" "secret-mgmt-baseline-sshPrivateKey"
  fi
    ;;
  create|update)
    az_manage_ssh_credentials || return $?
    ;;
esac
