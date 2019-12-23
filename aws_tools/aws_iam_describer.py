#!usr/bin/python3.7
"""Usage: python3 aws_iam_describer.py -h """
import argparse
import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import OperationNotPageableError
from tabulate import tabulate

# Parser for command line arguments
parser = argparse.ArgumentParser(prog="python3 aws_iam_describer.py",
                                 description="This is a script to show AWS IAM users and what privileges they have.")
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
                    help="If used, will output the details of the IAM Roles to std out")
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


def iam_describer():
    """This function handles finding and printing IAM """
    try:
        total_count = 0
        output_list = []
        headers = ["No.", "Role Name", "Resources", "Actions"]

        # The IAM boto3 client
        iam_client = session.client('iam', region_name=args.region)

        # Use a paginator since the AWS API defaults results to 50, with a max of 100
        iam_paginator = iam_client.get_paginator('list_roles')
        # Set the paginator to the max AWS API result of 100
        iam_page_iterator = iam_paginator.paginate(PaginationConfig={'PageSize': 100})

        # Filter only IAM Roles that have a last used date within the past 'x' amount of time
        iam_filtered_iterator = iam_page_iterator.search(f"Roles[] | [?RoleLastUsed.LastUsedDate != ``]")

        for iam in iam_filtered_iterator:
            total_count += 1
            output_list.append([total_count, iam['RoleName'], 'IDK', ''])

        print(f"Total IAM Roles: {total_count}")

        # If the output flag is set, then print details
        if args.output:
            # List the AutoScaling Groups that actually scale
            print("***************************************************************************************************")
            print(tabulate(output_list, headers))
            if total_count == 0:
                print("NONE!")
    except ClientError as ce:
        print(f"ERROR! ClientError: {ce}")
    except OperationNotPageableError as pe:
        print(f"ERROR! OperationNotPageableError: {pe}")


if __name__ == '__main__':
    """The Main function"""
    print(f"Checking The AWS Account For {args.profile} In Region {args.region} . . . ")
    iam_describer()
