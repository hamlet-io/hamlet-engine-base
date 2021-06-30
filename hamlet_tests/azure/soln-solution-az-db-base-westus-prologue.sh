#!/usr/bin/env bash
#--Hamlet-RequestReference=SRVREQ01
#--Hamlet-ConfigurationReference=configRef_v123
#--Hamlet-RunId=runId098
  # Check Keyvault for Master Secret
  if [[ $(az_check_secret "mockName" "mockedup-int-db-database-secret") = *SecretNotFound* ]]; then
   info "Generating Master Password... "
   master_password=""
   while ! [[ "${master_password}" =~ [[:alpha:]] && "${master_password}" =~ [[:digit:]] ]]; do
   master_password="$(generateComplexString "20" )"
   done
   info "Uploading Master Password to Keyvault... "
    az_add_secret "mockName" "mockedup-int-db-database-secret" "${master_password}" || return $?
  #
create_pseudo_stack "DB Master Secret" "${CF_DIR}/$(fileBase "${BASH_SOURCE}")-secret-pseudo-stack.json" "postgresdbXdbXdatabaseXsecret" "mockedup-int-db-database-secret" "Subscription" "0123456789" "ResourceGroup" "mockedup-integration-default-soln-solution-az-db-base" "Region" "westus" "DeploymentUnit" "solution-az-db-base" "DeploymentMode" "update"  || return $?
fi
