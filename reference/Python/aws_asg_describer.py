#!usr/bin/python3.7
import argparse
import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import OperationNotPageableError

# Argument Parser for command line
parser = argparse.ArgumentParser(prog="python3 aws_asg_describer.py",
                                 description="This is a script to show scaling details of AWS AutoScaling Groups.")
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
                    help="If used will output the details of the AutoScaling Groups")
parser.add_argument("-r",
                    "--region",
                    dest="region",
                    required=False,
                    default="us-east-1",
                    help="The AWS region to check. Defaults to us-east-1")
# Parse the arguments
args = parser.parse_args()

# Set the Boto3 session
session = boto3.Session(profile_name=args.profile)


def asg_describer():
    """This function handles finding and printing ASG's that actually scale, or don't scale"""
    total_count = 0
    scale_count = 0
    dont_scale_count = 0
    scale_list = []
    dont_scale_list = []

    try:
        # The ASG boto3 client
        asg_client = session.client('autoscaling', region_name=args.region)
        # Use a paginator since the AWS API defaults results to 50, with a max of 100
        paginator = asg_client.get_paginator('describe_auto_scaling_groups')
        # Set the paginator to the max AWS API result of 100
        page_iterator = paginator.paginate(PaginationConfig={'PageSize': 100})

        # Filter only ASG's that have at least 1 instance
        filtered_iterator = page_iterator.search("AutoScalingGroups[] | [?MaxSize > `0`]")

        for asg in filtered_iterator:
            total_count += 1
            name = asg["AutoScalingGroupName"]
            min_size = asg["MinSize"]
            max_size = asg["MaxSize"]
            desired = asg["DesiredCapacity"]
            if min_size == max_size:
                dont_scale_count += 1
                dont_scale_list.append([name, min_size, max_size, desired])
            else:
                scale_count += 1
                scale_list.append([name, min_size, max_size, desired])

        print(f"Total ASG's: {total_count}")
        print(f"ASG's that CAN Scale (Imagine That): {scale_count}")
        print(f"ASG's that DO NOT Scale (WHY?): {dont_scale_count}")

        # List the ASG's that actually scale
        if args.output:
            print("***************************************************")
            print("AutoScaling Groups That CAN Scale")
            for scale in scale_list:
                print(f"Name: {scale[0]}")
                print(f"    Min: {scale[1]}, Max: {scale[2]}, Desired: {scale[3]}")

            print("***************************************************")
            print("AutoScaling Groups That DO NOT Scale")
            for no_scale in dont_scale_list:
                print(f"Name: {no_scale[0]}")
                print(f"    Min: {no_scale[1]}, Max: {no_scale[2]}, Desired: {no_scale[3]}")

    except ClientError as ce:
        print(f"ERROR! ClientError: {ce}")
    except OperationNotPageableError as pe:
        print(f"ERROR! OperationNotPageableError: {pe}")


if __name__ == '__main__':
    """The Main function"""
    print(f"Checking the AWS account for {args.profile} in region {args.region}")
    asg_describer()
