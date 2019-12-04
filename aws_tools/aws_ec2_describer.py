#!usr/bin/python3.7
"""Usage: python3 aws_ec2_describer.py -h """
import argparse
import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import OperationNotPageableError

# Parser for command line arguments
parser = argparse.ArgumentParser(prog="python3 aws_ec2_describer.py",
                                 description="This is a script to show the details of EC2 instances within a given "
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
# Parse the arguments
args = parser.parse_args()

# Set the Boto3 session
session = boto3.Session(profile_name=args.profile)


def ec2_describer():
    """ This function handles describing ec2 instances """
    # TODO: find instance running for a long time, volumes that have existed for a long time, volumes that are not
    # TODO: attached to any instance, and anything else that might be sketch.


if __name__ == '__main__':
    """The Main function"""
    print(f"Checking the AWS account for {args.profile} in region {args.region} . . . ")
    ec2_describer()
