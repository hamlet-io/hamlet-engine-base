#!/usr/bin/env bash
#--Hamlet-RequestReference=SRVREQ01
#--Hamlet-ConfigurationReference=configRef_v123
#--Hamlet-RunId=runId098
 # AAD App Registration
 case ${DEPLOYMENT_OPERATION} in
   delete)
       # Remove AAD App Registration
       info "No App Registration Identifier Found. Skipping."
       ;;
   create|update)
       az ad app create  > $tmp/registration.json
       objectId=$(runJQ -r '.objectId' < $tmp/registration.json)
       clientId=$(runJQ -r '.appId' < $tmp/registration.json)
