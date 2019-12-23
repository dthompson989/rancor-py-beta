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


def ec2_describer():
    """ This function handles describing ec2 instances that have some kind of issue that needs addressing, such as
        instances that have been running for a long time and (maybe) out of date ami's """
    try:
        # These variables are for instances that have issues
        total_ec2 = 0
        long_running_ec2 = 0
        outdated_ami = 0
        ec2_detail_list = []

        print(f"Total EC2's with Issues: {total_ec2}")
        print(f"EC2's That Have Been Running For A Long Time: {long_running_ec2}")
        print(f"Outdated AMI's: {outdated_ami}")

        # If the output flag is set, then print details
        if args.output:
            # List the problem EC2 Instances
            print("***************************************************************************************************")
            print("EC2 Instances with an issue that needs addressing . . . ")

    except ClientError as ce:
        print(f"ERROR! ClientError: {ce}")
    except OperationNotPageableError as pe:
        print(f"ERROR! OperationNotPageableError: {pe}")


if __name__ == '__main__':
    """The Main function"""
    print(f"Checking The AWS Account For {args.profile} In Region {args.region} . . . ")
    ec2_describer()
    # TODO: Potentially combine all of these scripts, if it can be done in a reasonable way.
