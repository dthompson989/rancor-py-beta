#!usr/bin/python3.7
"""Usage: python3 aws_lambda_describer.py -h """
import argparse
import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import OperationNotPageableError

# Parser for command line arguments
parser = argparse.ArgumentParser(prog="python3 aws_lambda_describer.py",
                                 description="This is a script to show the details of Lambda functions within a given "
                                             "account and region. It will output a list of all the Lambda functions "
                                             "that are using a deprecated (or soon to be deprecated) code version, "
                                             "functions that have no tags, and functions that have not been run in "
                                             "a long time. IMPORTANT NOTE: This is a command line tool, it has not been"
                                             "converted for AWS Lambda use.")
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
                    help="If used, will output the details of the Lambda functions")
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


def lambda_describer():
    """ This function handles describing lambda functions that have some kind of issue that needs addressing, such as
        deprecated, or soon to be deprecated versions, no tags, and not have run in more than x amount of time. """
    try:
        # These variables are for volumes that have issues
        deprecated_version_list = ["python2.7", "nodejs", "nodejs4.3", "nodejs4.3-edge", "nodejs6.10", "dotnetcore2.0",
                                   "dotnetcore1.0", "nodejs8.10", "ruby2.4", "ruby2.3", "ruby2.2"]
        total_lambdas = 0
        outdated_lambdas = 0
        unused_lambdas = 0
        untagged_lambdas = 0
        lambda_detail_list = []

        # The Lambda function boto3 client
        lambda_client = session.client('lambda', region_name=args.region)

        # Use a paginator since the AWS API defaults results to 50, with a max of 100
        lambda_paginator = lambda_client.get_paginator('list_functions')
        # Set the paginator to the max AWS API result of 100
        lambda_page_iterator = lambda_paginator.paginate(PaginationConfig={'PageSize': 100})

        for page in lambda_page_iterator:
            for f in page['Functions']:
                name = f['FunctionName']
                runtime = f['Runtime']
                arn = f['FunctionArn']
                issues = []

                if runtime in deprecated_version_list:
                    outdated_lambdas += 1
                    issues.append("Deprecated Version")

                # Check for tags
                function_tags = lambda_client.list_tags(Resource=arn)
                if len(function_tags['Tags']) == 0:
                    untagged_lambdas += 1
                    issues.append("No Tags")

                # Check when the last time this lambda ran, and if it was successful

                if len(issues) > 0:
                    total_lambdas += 1
                    lambda_detail_list.append([name, runtime, issues])

        # If the output flag is set, then print details
        if args.output:
            # List the problem EBS volumes
            print("***************************************************************************************************")
            print("Lambda functions with an issue that needs addressing . . . \n")
            s = " ::: "
            for detail in lambda_detail_list:
                print(f"NAME: {detail[0]}")
                print(f"    RUNTIME: {detail[1]}")
                print(f"    ISSUES: {s.join(detail[2])}")

        if total_lambdas == 0:
            print("NONE!")

        print("\n***************************************************************************************************\n")
        print(f"Total Lambda Functions With Issues: {total_lambdas}")
        print(f"Lambda Functions That Have Not Been Used For A Long Time: {unused_lambdas} (This is not implemented)")
        print(f"Untagged Lambda Functions: {untagged_lambdas}")
        print(f"Outdated Lambda Function: {outdated_lambdas}\n")

    except ClientError as ce:
        print(f"ERROR! ClientError: {ce}")
    except OperationNotPageableError as pe:
        print(f"ERROR! OperationNotPageableError: {pe}")


if __name__ == '__main__':
    """The Main function"""
    print(f"Checking The AWS Account For {args.profile} In Region {args.region} . . . ")
    lambda_describer()
