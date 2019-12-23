#!usr/bin/python3.7
"""Usage: python3 aws_cloudformation_describer.py -h """
import argparse
import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import OperationNotPageableError
from tabulate import tabulate
import pprint

# Parser for command line arguments
parser = argparse.ArgumentParser(prog="python3 aws_cloudformation_describer.py",
                                 description="This is a script to show AWS CloudFormation stacks and what privileges "
                                             "they have.")
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
                    help="If used, will output the details of the CloudFormation Stacks to std out")
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


def cf_describer():
    """This function handles finding and printing CloudFormation Stack information """
    try:
        total_count = 0
        output_list = []
        headers = ["Stack Name", "Tags"]
        pp = pprint.PrettyPrinter()

        # The CloudFormation boto3 client
        cf_client = session.client('cloudformation', region_name=args.region)

        # Use a paginator since the AWS API defaults results to 50, with a max of 100
        cf_paginator = cf_client.get_paginator('describe_stacks')
        # Set the paginator to the max AWS API result of 100
        params = {'StackName': 'ddc4-csr-iam'}
        cf_page_iterator = cf_paginator.paginate(**params)

        # Filter only stacks that have been successfully created
        cf_filtered_iterator = cf_page_iterator.search(f"Stacks[] | [?StackStatus == `CREATE_COMPLETE`]")

        for stack in cf_filtered_iterator:
            total_count += 1
            # print(pp.pprint(stack)) # DEBUGGING
            output_list.append([stack['StackName'], stack['Tags']])

        print(f"Total Stacks: {total_count}")

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
    print(f"Checking The AWS Account For {args.profile} In Region {args.region} . . . \n")
    cf_describer()
    # TODO: It might be worth it to add a master orchestration script to join some of these together.
