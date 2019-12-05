#!usr/bin/python3.7
"""Usage: python3 aws_rds_describer.py -h """
import argparse
import boto3
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
                    help="If used, will output the details of the AutoScaling Groups")
parser.add_argument("-r",
                    "--region",
                    dest="region",
                    required=False,
                    default="us-east-1",
                    help="The AWS region to check. Default is us-east-1")
# Parse the arguments
args = parser.parse_args()

# Set the Boto3 session
session = boto3.Session(profile_name=args.profile)


def rds_describer():
    """ This function handles describing RDS databases that have some kind of issue that needs addressing, such as
        outdated database versions, non production databases that are not used, and (maybe) databases that have/need
        maintenance soon. """
    try:
        # These variables are for volumes that have issues
        total_rds = 0
        outdated_version = 0
        unused_rds = 0
        rds_maint = 0
        rds_detail_list = []

        # The RDS boto3 client
        rds_client = session.client('rds', region_name=args.region)

        # Use a paginator since the AWS API defaults results to 100, with a max of 100
        rds_paginator = rds_client.get_paginator('describe_db_instances')
        # Set the paginator to the max AWS API result of 100
        rds_page_iterator = rds_paginator.paginate(PaginationConfig={'PageSize': 100})

        for db in rds_page_iterator["DBInstances"]:
            db_id = db["DBInstanceIdentifier"]
            version = db["EngineVersion"]
            lastest_restore = db["LatestRestorableTime"]

            pending_action_response = rds_client.describe_pending_maintenance_actions(
                Filters=[{'Name': 'db-instance-id', 'Values': [db_id]}])

            if pending_action_response:
                total_rds += 1
                rds_maint += 1
                rds_detail_list.append([db_id, version, lastest_restore])

        print(f"Total RDS Databases with Issues: {total_rds}")
        print(f"RDS Databases with Outdated Versions: {outdated_version}")
        print(f"Unused Non Prod RDS Databases: {unused_rds}")
        print(f"RDS Databases with Upcoming Maintenance: {rds_maint}")

        # If the output flag is set, then print details
        if args.output:
            # List the problem EBS volumes
            print("***************************************************************************************************")
            print("RDS Databases with an issue that needs addressing . . . ")

    except ClientError as ce:
        print(f"ERROR! ClientError: {ce}")
    except OperationNotPageableError as pe:
        print(f"ERROR! OperationNotPageableError: {pe}")


if __name__ == '__main__':
    """The Main function"""
    print(f"Checking The AWS Account For {args.profile} In Region {args.region} . . . ")
    rds_describer()
    # TODO: Potentially combine all of these scripts, if it can be done in a reasonable way.
