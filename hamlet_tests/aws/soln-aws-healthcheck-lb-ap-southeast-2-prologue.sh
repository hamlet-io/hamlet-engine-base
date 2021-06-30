#!/usr/bin/env bash
#--Hamlet-RequestReference=SRVREQ01
#--Hamlet-ConfigurationReference=configRef_v123
#--Hamlet-RunId=runId098
create_pseudo_stack "CLI Rule Cleanup" "${CF_DIR}/$(fileBase "${BASH_SOURCE}")-pseudo-stack.json" "listenerXelbXhealthchecklbXhttpsXcleanup" "true" "listenerXelbXhealthchecklbXhttpXcleanup" "true" "Account" "0123456789" "Region" "ap-southeast-2" "DeploymentUnit" "aws-healthcheck-lb-prologue" "DeploymentMode" "update"  || return $?
