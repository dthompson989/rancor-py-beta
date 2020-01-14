#!usr/bin/python3.7
"""Usage: python3 aws_iam_describer.py -h"""
import argparse
import boto3
import pickle
from botocore.exceptions import ClientError
from botocore.exceptions import OperationNotPageableError
from tabulate import tabulate

# Parser for command line arguments
parser = argparse.ArgumentParser(prog="python3 aws_iam_describer.py",
                                 description="NOTICE: THIS FUNCTION HAS BEEN DEPRICATED! "
                                             "This is a script to show AWS IAM users, what policies they have, and "
                                             "generate a services access report in AWS. The Job ID is printed out and "
                                             "is also stored in the file jobs_list_file.data along with the IAM "
                                             "Role Name. This should be used with aws_jobs_describer.py which will "
                                             "get the details of the job requests and output whatever results exist. "
                                             "The AWS jobs reports can take a little time to complete, so "
                                             "aws_jobs_describer.py should be run a while after this script. ")
# Add parser arguments
parser.add_argument("-p",
                    "--profile",
                    dest="profile",
                    required=True,
                    help="REQUIRED. The AWS profile name to use.")
parser.add_argument("-o",
                    "--output",
                    dest="output",
                    action="store_true",
                    default=False,
                    help="If set, will output the details of the IAM Roles to std out.")
parser.add_argument("-r",
                    "--region",
                    dest="region",
                    required=False,
                    default="us-east-1",
                    help="The AWS region to check. Default is us-east-1.")
parser.add_argument("-v",
                    "--verbose",
                    dest="verbose",
                    action="store_true",
                    default=False,
                    help="If set, will output ALL IAM roles. The default is only a subset of IAM roles (Currently only "
                         "the top 10 IAM roles returned).")
# Parse the arguments
args = parser.parse_args()
# The config for the paginator, limit to only 10 results unless in verbose mode
pagination_config = {'PageSize': 100} if args.verbose else {'PageSize': 10, 'MaxItems': 10}
# Set the Boto3 session
session = boto3.Session(profile_name=args.profile)
# The IAM boto3 client
iam_client = session.client('iam', region_name=args.region)


def iam_describer():
    """This function handles finding and printing IAM """
    try:
        total_count = 0
        output_list = list()
        jobs_dict = dict()
        headers = ["No.", "Role Name", "Service Last Accessed Job Id"]
        # Use a paginator since the AWS API defaults results to 50, with a max of 100
        iam_paginator = iam_client.get_paginator('list_roles')
        # The pagination iterator, will either be all IAM roles, or just 10 depending on verbosity
        iam_page_iterator = iam_paginator.paginate(PaginationConfig=pagination_config)
        # Filter only IAM Roles that have a last used date within the past 'x' amount of time
        iam_filtered_iterator = iam_page_iterator.search(f"Roles[] | [?RoleLastUsed.LastUsedDate != ``]")

        for iam in iam_filtered_iterator:
            iam_role_name = iam['RoleName']
            iam_role_arn = iam['Arn']
            job_id = "None"

            # Generate a Service Last Accessed Report, these can take a little while, so we will save to a binary doc
            # for another script to use. You can also perform an additional search using
            # GetServiceLastAccessedDetailsWithEntities and inputting the job id and the AWS service namespace.
            job_response = iam_client.generate_service_last_accessed_details(Arn=iam_role_arn)
            if job_response['JobId']:
                job_id = job_response['JobId']
                jobs_dict[iam_role_name] = job_id

            total_count += 1
            output_list.append([total_count, iam_role_name, job_id])

        # Save the jobs id's to a binary data file using pickle
        with open('jobs_list_file.data', 'wb') as file_handle:
            pickle.dump(jobs_dict, file_handle)

        print(f"Total IAM Roles: {total_count}")
        # If the output flag is set, then print details
        if args.output:
            # List the AutoScaling Groups that actually scale
            print("\n*************************************************************************************************")
            print(tabulate(output_list, headers, tablefmt="grid"))
            if total_count == 0:
                print("NONE!")
    except ClientError as ce:
        print(f"ERROR! ClientError: {ce}")
    except OperationNotPageableError as pe:
        print(f"ERROR! OperationNotPageableError: {pe}")
    except pickle.PickleError as pickle_error:
        print(f"ERROR: PickleError {pickle_error}")


if __name__ == '__main__':
    """The Main function"""
    print(f"Checking The AWS Account For {args.profile} In Region {args.region} . . . ")
    iam_describer()
