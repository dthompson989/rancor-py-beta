#!usr/bin/python3.7
"""Usage: python3 aws_asg_describer.py -h """
import argparse
import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import OperationNotPageableError

# Parser for command line arguments
parser = argparse.ArgumentParser(prog="python3 aws_asg_describer.py",
                                 description="This is a script to show the scaling details of AWS AutoScaling Groups. "
                                             "Depending on the account you are checking, it can take a few seconds to "
                                             "run. The assumption is AutoScaling Groups that have the same MIN and MAX"
                                             " are not able to scale, and probably do not have any scaling policies "
                                             "associated with them. The AutoScaling groups that have a different MIN "
                                             "and MAX might be able to scale properly, if they also have scaling "
                                             "policies attached to them.")
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


def asg_describer():
    """This function handles finding and printing AutoScaling Groups that can scale, or don't scale at all"""
    try:
        total_count = 0
        scale_count = 0
        dont_scale_count = 0
        scale_list = []
        dont_scale_list = []

        # The AutoScaling Group boto3 client
        asg_client = session.client('autoscaling', region_name=args.region)

        # Use a paginator since the AWS API defaults results to 50, with a max of 100
        asg_paginator = asg_client.get_paginator('describe_auto_scaling_groups')
        # Set the paginator to the max AWS API result of 100
        asg_page_iterator = asg_paginator.paginate(PaginationConfig={'PageSize': 100})

        # Filter only AutoScaling Groups that have at least 1 instance max size
        asg_filtered_iterator = asg_page_iterator.search("AutoScalingGroups[] | [?MaxSize > `0`]")

        for asg in asg_filtered_iterator:
            total_count += 1
            name = asg["AutoScalingGroupName"]
            min_size = asg["MinSize"]
            max_size = asg["MaxSize"]
            desired = asg["DesiredCapacity"]
            policies = []

            # If --output flag was set, then check if there is a scaling policy for this AutoScaling Group
            if args.output:
                # Searching for policies this way is faster than searching using a paginator and filter (VERY slow).
                policy = asg_client.describe_policies(AutoScalingGroupName=name)
                if policy:
                    for p in policy['ScalingPolicies']:
                        policies.append([p["PolicyName"], p["PolicyType"], p["AdjustmentType"]])

            # If the min and max are the same, then it can't scale
            if min_size == max_size:
                dont_scale_count += 1
                dont_scale_list.append([name, min_size, max_size, desired, policies])
            else:
                scale_count += 1
                scale_list.append([name, min_size, max_size, desired, policies])

        print(f"Total ASG's: {total_count}")
        print(f"ASG's that CAN Scale (Imagine That): {scale_count}")
        print(f"ASG's that DO NOT Scale (WHY?): {dont_scale_count}")

        # If the output flag is set, then print details
        if args.output:
            # List the AutoScaling Groups that actually scale
            print("***************************************************************************************************")
            print("AutoScaling Groups That CAN Scale")
            for scale in scale_list:
                print(f"NAME: {scale[0]}")
                print(f"    Min: {scale[1]}, Max: {scale[2]}, Desired: {scale[3]}")
                for p in scale[4]:
                    print(f"    POLICY: {p[0]} ::: {p[1]} ::: {p[2]}")
            if scale_count == 0:
                print("NONE!")

            # List the AutoScaling Groups that don-t scale
            print("***************************************************************************************************")
            print("AutoScaling Groups That DO NOT Scale")
            for no_scale in dont_scale_list:
                print(f"Name: {no_scale[0]}")
                print(f"    Min: {no_scale[1]}, Max: {no_scale[2]}, Desired: {no_scale[3]}")
            if dont_scale_count == 0:
                print("NONE!")

    except ClientError as ce:
        print(f"ERROR! ClientError: {ce}")
    except OperationNotPageableError as pe:
        print(f"ERROR! OperationNotPageableError: {pe}")


if __name__ == '__main__':
    """The Main function"""
    print(f"Checking the AWS account for {args.profile} in region {args.region} . . . ")
    asg_describer()
