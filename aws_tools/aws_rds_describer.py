#!usr/bin/python3.7
"""Usage: python3 aws_rds_describer.py -h """
import argparse
import boto3
import pprint
from tabulate import tabulate
from botocore.exceptions import ClientError
from botocore.exceptions import OperationNotPageableError

# Parser for command line arguments
parser = argparse.ArgumentParser(prog="python3 aws_rds_describer.py",
                                 description="This is a script to show the details of RDS databases within a given "
                                             "account and region that have some issues that need addressing.")
# Add parser arguments
parser.add_argument("-p",
                    "--profile",
                    dest="profile",
                    required=True,
                    help="REQUIRED. The AWS profile name to use")
parser.add_argument("-o",
                    "--output",
                    dest="output",
                    action="store_true",
                    default=False,
                    help="If used, will output the details of RDS")
parser.add_argument("-r",
                    "--region",
                    dest="region",
                    required=False,
                    default="us-east-1",
                    help="The AWS region to check. Default is us-east-1")
# Parse the arguments
args = parser.parse_args()

# Set the boto3 session
session = boto3.Session(profile_name=args.profile)
# The RDS boto3 client
rds_client = session.client('rds', region_name=args.region)


def db_version_checker(engine, version):
    """ This is a helper function used in rds_describer(). It checks to see if the given database engine can/should
        be upgraded. """
    upgrade_list = []
    version_response = rds_client.describe_db_engine_versions(Engine=engine, EngineVersion=version)
    for upgrade in version_response["DBEngineVersions"][0]["ValidUpgradeTarget"]:
        upgrade_list.append([upgrade['Engine'], upgrade['EngineVersion']])

    return upgrade_list


def rds_describer():
    """ This function handles describing RDS databases that have some kind of issue that needs addressing, such as
        outdated database versions, non production databases that are not used, and (maybe) databases that have/need
        maintenance soon. """
    try:
        # These variables are for volumes that have issues
        total_rds = 0
        outdated_version = 0
        unused_rds = 0
        rds_maintenance = 0
        rds_modifications = 0
        rds_issues_list = []
        # Use a pretty printer for printing list of lists
        pp = pprint.PrettyPrinter()
        # Use a paginator since the AWS API defaults results to 100, with a max of 100
        rds_paginator = rds_client.get_paginator('describe_db_instances')
        # Set the paginator to the max AWS API result of 100
        rds_page_iterator = rds_paginator.paginate(PaginationConfig={'PageSize': 100})

        for pages in rds_page_iterator:
            for db in pages['DBInstances']:
                db_name = db['DBInstanceIdentifier']
                engine = db['Engine']
                version = db['EngineVersion']
                pending_modifications = db['PendingModifiedValues']
                pending_list = []

                # Check if there is a version upgrade available
                upgrade_available = db_version_checker(engine, version)
                # Check if there are pending maintenance
                pending_action_response = rds_client.describe_pending_maintenance_actions(
                    Filters=[{'Name': 'db-instance-id', 'Values': [db_name]}])

                if upgrade_available:
                    outdated_version += 1
                if pending_modifications:
                    rds_modifications += 1
                if pending_action_response:
                    rds_maintenance += 1
                    for p in pending_action_response['PendingMaintenanceActions']:
                        for a in p['PendingMaintenanceActionDetails']:
                            pending_list.append(a['Action'])

                if upgrade_available or pending_action_response or pending_modifications:
                    total_rds += 1
                    rds_issues_list.append([db_name, engine, version, tabulate(upgrade_available, tablefmt="plain"),
                                            pp.pformat(pending_list), pp.pformat(pending_modifications)])

        # If the output flag is set, then print details
        if args.output:
            # List the problem EBS volumes
            print("\n***********************************************************************************************\n")
            print("RDS Databases with an issue that needs addressing . . . \n")
            headers = ["DB Name", "Engine", "Current Version", "Version Upgrade Available",
                       "Pending Maintenance", "Pending Modifications"]
            print(tabulate(rds_issues_list, headers, tablefmt="grid"))
        if total_rds == 0:
            print("NONE!")

        print(f"\nTotal RDS Databases with Issues: {total_rds}")
        print(f"RDS Databases with Outdated Versions: {outdated_version}")
        print(f"RDS Databases with Upcoming Maintenance: {rds_maintenance}")
        print(f"RDS Databases with Pending Modifications: {rds_modifications}")
        print(f"Unused Non Prod RDS Databases: {unused_rds}\n")

    except ClientError as ce:
        print(f"ERROR! ClientError: {ce}")
    except OperationNotPageableError as pe:
        print(f"ERROR! OperationNotPageableError: {pe}")


if __name__ == '__main__':
    """The Main function"""
    print(f"Checking The AWS Account For {args.profile} In Region {args.region} . . . ")
    rds_describer()
