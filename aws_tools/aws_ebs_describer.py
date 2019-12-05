#!usr/bin/python3.7
"""Usage: python3 aws_ebs_describer.py -h """
import argparse
import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import OperationNotPageableError

# Parser for command line arguments
parser = argparse.ArgumentParser(prog="python3 aws_ebs_describer.py",
                                 description="This is a script to show the details of EBS volumes within a given "
                                             "account and region.")
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
parser.add_argument("-l",
                    "--limit",
                    dest="limit",
                    required=False,
                    type=int,
                    help="Limit the search results")
# Parse the arguments
args = parser.parse_args()

# Set the Boto3 session
session = boto3.Session(profile_name=args.profile)


def ebs_describer():
    """ This function handles describing ebs volumes that have some kind of issue that needs addressing, such as
        ebs volumes that have existed for a long time and ebs volumes that are not used. """
    try:
        # These variables are for volumes that have issues
        total_ebs = 0
        long_running_ebs = 0
        unused_ebs = 0
        ebs_detail_list = []

        # If the output flag is set, then print details
        if args.output:
            # List the problem EBS volumes
            print("***************************************************************************************************")
            print("EBS Volumes with an issue that needs addressing . . . ")

    except ClientError as ce:
        print(f"ERROR! ClientError: {ce}")
    except OperationNotPageableError as pe:
        print(f"ERROR! OperationNotPageableError: {pe}")


if __name__ == '__main__':
    """The Main function"""
    print(f"Checking The AWS Account For {args.profile} In Region {args.region} . . . ")
    ebs_describer()
    # TODO: Potentially combine all of these scripts, if it can be done in a reasonable way.
