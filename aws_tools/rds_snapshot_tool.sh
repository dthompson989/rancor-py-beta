#!/bin/bash
# Usage: sh rds_snapshot_tool.sh -p my-local-aws-profile-name -r 'us-east-1' -t 'cluster' -d 'demo-db-cluster' -s 'demo-db-snapshot' -a '123456789012'
#   profile (-p): This is the AWS profile you want to use
#   region (-r): This is the region the database is located in
#   type (-t): Is this a databse cluster or an instance
#   database identifier (-d): The database/cluster identifier
#   snapshot identifier (-s): The name of the snapshot identifer to create
#   account to share with(-a): (Optional) The account number you want to share the snapshot with
#   HELP (-h): The usage function output
#
#   *** NOTE: This script uses JQ, a JSON processing tool

# Script variables
share_account=false
snapshot_arn=''
profile=''
status='none'

###################################################################################################################
#### HELPER FUNCTIONS
###################################################################################################################
# A usage help function
usage() {
  echo "This tool is used to create an RDS snapshot from either an instance or cluster resource, and has the option to share the snapshot with another account"
  echo ""
  echo "Syntax: sh rds_snapshot_tool.sh [-p|r|t|d|s|a|h]"
  echo ""
  echo "options:"
  echo "-r    The AWS REGION that the database is located in"
  echo "-t    The TYPE of database; either 'cluster' or 'instance'"
  echo "-d    The DATABASE identifier you want to make a snapshot of"
  echo "-s    The name you want to give to the SNAPSHOT"
  echo "-a    [OPTIONAL] The ACCOUNT number of an account you want to share the snapshot with"
  echo "-p    [OPTIONAL] The AWS PROFILE to use. You need to authenticate first, but you can set the AWS_PROFILE variable before running this script"
  echo "-h    [OPTIONAL] Print HELP usage"
  echo ""
  echo "Example: sh rds_snapshot_tool.sh -r 'us-east-1' -t 'cluster' -d 'demo-db-cluster' -s 'demo-db-snapshot' -a '123456789012'"
  echo ""
}

# Exit function for failures
exit_failure() {
  echo "$1"
  exit 1
}

# Exit function, which prints the usage help
exit_abnormal() {
  usage
  exit 1
}

# Help function
exit_help() {
  usage
  exit 0
}

###################################################################################################################
### START SCRIPT
###################################################################################################################
echo "Starting RDS Snapshot Tool Script"
echo ""
echo "Checking input . . . "
###################################################################################################################
### GRAB INPUT FLAGS/OPTIONS USING "GEt The OPTionS"
###################################################################################################################
while getopts ":r:t:d:s:a:p:h" flag;
do
  case "${flag}" in
    r) region="${OPTARG}";;
    t) db_type="${OPTARG}"
       if [ "${db_type}" != "cluster" ] && [ "${db_type}" != "instance" ]; then
         exit_abnormal
       fi;;
    d) db_id="${OPTARG}";;
    s) snapshot_id="${OPTARG}";;
    a) account_number="${OPTARG}"
       if [ "${account_number}" != "" ]; then
         share_account=true
       fi;;
    p) profile="${OPTARG}";;
    h) exit_help;;
    :) echo "Error: -${OPTARG} requires an argument."
       echo ""
       exit_abnormal;;
    /?) echo "Error: Invalid option"
        echo ""
        exit_abnormal;;
    *) exit_abnormal;;
  esac
done

# Check some of the input for blank args
if [ "${db_type}" = "" ] || [ "${db_id}" = "" ] || [ "${snapshot_id}" = "" ] || [ "${region}" = "" ]; then
  echo "Error: Invalid Empty Input"
  exit_abnormal
fi

###################################################################################################################
### BEGIN CREATE SNAPSHOT
###################################################################################################################
# Set the profile, if provided
if [ "${profile}" != "" ]; then
  echo "Using profile ${profile}"
  export AWS_PROFILE="${profile}"
fi
# Change to the specified region
echo "Setting AWS REGION to ${region}"
export AWS_DEFAULT_REGION="${region}"

###################################################################################################################
# Create RDS cluster snapshot (and share if needed)
if [ "${db_type}" = "cluster" ]; then
  # Begin the snapshot process
  echo "CREATING snapshot: ${snapshot_id} FROM database cluster: ${db_id} IN region: ${region}"
  # Response structure: ['DBClusterSnapshot'].['DBClusterSnapshotArn']
  snapshot_arn=$(aws rds create-db-cluster-snapshot --db-cluster-snapshot-identifier "${snapshot_id}" --db-cluster-identifier "${db_id}" | jq '.DBClusterSnapshot.DBClusterSnapshotArn')

  # Monitor the snapshot creation until it's available
  until [ "${status}" = '"available"' ]; do
    # Response structure: .['DBClusterSnapshots'].['Status']
    status=$(aws rds describe-db-cluster-snapshots --db-cluster-snapshot-identifier "${snapshot_id}" | jq '.DBClusterSnapshots[0] .Status')
    # If the snapshot isn't in the 'creating' or 'available' state then it failed
    if [ "${status}" != '"creating"' ] && [ "${status}" != '"available"' ]; then
      exit_failure "Error: SNAPSHOT FAILED! Status: ${status}"
    fi
    # Snapshots can take awhile so check back on it periodically
    sleep 60
    echo "Still CREATING Snapshot . . ."
  done

  # If we are sharing the snapshot with another account
  if [ "${share_account}" ] && [ "${account_number}" != "" ]; then
    echo "Sharing ${snapshot_id} with ${account_number}"
    aws rds modify-db-cluster-snapshot-attribute --db-cluster-snapshot-identifier "${snapshot_id}" --attribute-name restore --values-to-add "${account_number}"
  fi
###################################################################################################################
# Create RDS instance the snapshot (and share if needed)
elif [ "${db_type}" = "instance" ]; then
  # Begin the snapshot process
  echo "CREATING snapshot: ${snapshot_id} FROM database instance: ${db_id} IN region: ${region}"
  # Response structure: ['DBSnapshot'].['DBSnapshotArn']
  snapshot_arn=$(aws rds create-db-snapshot --db-instance-identifier "${db_id}" --db-snapshot-identifier "${snapshot_id}" | jq '.DBSnapshot.DBSnapshotArn')

  # Monitor the snapshot creation until it's available
  until [ "${status}" = '"available"' ]; do
    # Response structure: .['DBSnapshots'].['Status']
    status=$(aws rds describe-db-snapshots --db-snapshot-identifier "${snapshot_id}" | jq '.DBSnapshots[0] .Status')
    # If the snapshot isn't in the 'creating' or 'available' state then it failed
    if [ "${status}" != '"creating"' ] && [ "${status}" != '"available"' ]; then
      exit_failure "Error: SNAPSHOT FAILED! Status: ${status}"
    fi
    # Snapshots can take awhile so check back on it periodically
    sleep 60
    echo "Still CREATING Snapshot . . ."
  done

  # If we are sharing the snapshot with another account
  if [ "${share_account}" ] && [ "${account_number}" != "" ]; then
    echo "Sharing ${snapshot_id} with ${account_number}"
    aws rds modify-db-snapshot-attribute --db-snapshot-identifier "${snapshot_id}" --attribute-name restore --values-to-add "${account_number}"
  fi
###################################################################################################################
# Bad input
else
  echo "Error: Invalid DB_TYPE: ${db_type}"
  exit_abnormal
fi
###################################################################################################################
### SNAPSHOT CREATION COMPLETE
###################################################################################################################
echo "Snapshot creation complete: ${snapshot_arn}"
###################################################################################################################
### END SCRIPT
###################################################################################################################
exit 0