#!usr/bin/python3.7
"""Usage: python3 aws_attach_role_to_secret.py -h"""
import argparse
import boto3
import string
import random
from botocore.exceptions import ClientError

# Parser for command line arguments
parser = argparse.ArgumentParser(prog="python3 aws_attach_role_to_secret.py",
                                 description="")
# Add parser arguments
parser.add_argument("-p",
                    "--profile",
                    dest="profile",
                    required=True,
                    help="REQUIRED. The AWS profile name to use.")
parser.add_argument("-s",
                    "--secret",
                    dest="secret",
                    required=True,
                    help="REQUIRED. The Name of the secret.")
parser.add_argument("-f",
                    "--file",
                    dest="file",
                    required=True,
                    help="REQUIRED. The JSON file name of the IAM Role.")
# Parse the arguments
args = parser.parse_args()
# Set the Boto3 session
session = boto3.Session(profile_name=args.profile)
# The IAM boto3 client
secrets_client = session.client('secretsmanager')


def attach_role():
    """This function handles attaching the IAM policy document to the Secrets Manager Secret"""
    try:
        file_name = args.file
        # TODO: Finish this function
        sts_role_session_name = "lambda-cross-account-session-" + \
                                ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
        print(f"Session Name: {sts_role_session_name}")
    except ClientError as ce:
        print(f"ERROR! ClientError: {ce}")


if __name__ == '__main__':
    """The Main function"""
    print(f"Checking The AWS Account For {args.profile} . . . ")
    attach_role()
