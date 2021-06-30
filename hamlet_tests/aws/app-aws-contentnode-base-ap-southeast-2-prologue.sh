#!/usr/bin/env bash
#--Hamlet-RequestReference=
#--Hamlet-ConfigurationReference=
#--Hamlet-RunId=0w6w2h1pru
function get_contentnode_file_appXcontentnodebase() {
  # Fetch the spa zip file
  copyFilesFromBucket ap-southeast-2 account-registry-abc123 contentnode/mockedup/aws-contentnode-base/123456789#MockCommit#  "${tmpdir}" || return $?
  # Sync with the contentnode
  copy_contentnode_file "${tmpdir}/contentnode.zip" "github" "" "/" "mockedup-default" "master" "replace" || return $? 
}
get_contentnode_file_appXcontentnodebase || exit $?
