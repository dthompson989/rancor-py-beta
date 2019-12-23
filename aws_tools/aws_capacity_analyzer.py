#!usr/bin/python3.7
"""Usage: python3 aws_capacity_analyzer.py -h """
import argparse
import boto3
import pprint
from botocore.exceptions import ClientError
from botocore.exceptions import OperationNotPageableError

# Parser for command line arguments
parser = argparse.ArgumentParser(prog="python3 aws_capacity_analyzer.py",
                                 description="This is a script to show the details of Reserve Instances within a given "
                                             "account and region. It will output a list of how many RI's we have by "
                                             "instance type, and how many are being used. ")
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
                    help="If used, will output the details of the Reserve Instances")
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


def reserve_describer():
    """ This function handles describing Reserve Instance details, like how many of each instance type are reserved
        and how many instance of that type are running. """
    try:
        # These variables are for volumes that have issues
        ri_detail_list = {}

        # The Lambda function boto3 client
        ec2_client = session.client('ec2', region_name=args.region)
        ri_filter = [{'Name': 'state', 'Values': ['active']}]
        # Use a paginator since the AWS API defaults results to 50, with a max of 100
        ec2_ri_dict = ec2_client.describe_reserved_instances(Filters=ri_filter)

        for ri in ec2_ri_dict['ReservedInstances']:
            instance_type = ri['InstanceType']
            ri_count = ri['InstanceCount']
            platform = ri['ProductDescription']
            if instance_type in ri_detail_list:
                ri_detail_list[instance_type]['Reserve Instances'] += ri_count
            else:
                ri_detail_list[instance_type] = {'Reserve Instances': ri_count,
                                                 'EC2 Instances': 0}

        # If the output flag is set, then print details
        if args.output:
            print("***************************************************************************************************")
            print("Active Reserve Instance Details . . . \n")
            for key, value in ri_detail_list.items():
                print(f"Instance Type: {key}")
                for key2, value2 in value.items():
                    print(f"    {key2}: {value2}")

        print("\n***************************************************************************************************\n")

    except ClientError as ce:
        print(f"ERROR! ClientError: {ce}")
    except OperationNotPageableError as pe:
        print(f"ERROR! OperationNotPageableError: {pe}")


if __name__ == '__main__':
    """The Main function"""
    print(f"Checking The AWS Account For {args.profile} In Region {args.region} . . . ")
    reserve_describer()
