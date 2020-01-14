#!usr/bin/python3.7
"""Usage: python3 aws_iam_auditor.py -h """
import argparse
import boto3
import pprint
import json
from botocore.exceptions import ClientError
from tabulate import tabulate

# Parser for command line arguments
parser = argparse.ArgumentParser(prog="python3 aws_iam_auditor.py",
                                 description="This is a script to show AWS IAM Roles, what they CAN access, and "
                                             "finally what they actually are accessing. This is used to audit AWS "
                                             "IAM roles and policies to help provide context to the principle of "
                                             "least privilege to the services using them.")
# Add parser arguments
parser.add_argument("-p",
                    "--profile",
                    dest="profile",
                    required=True,
                    help="REQUIRED. The AWS profile name to use.")
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
parser.add_argument("-d",
                    "--debug",
                    dest="debug",
                    action="store_true",
                    default=False,
                    help="If set, turns on debugging. The default is False")
# Parse the arguments
args = parser.parse_args()
# Use a pretty printer for printing list of lists
pp = pprint.PrettyPrinter()
# Set the Boto3 session
session = boto3.Session(profile_name=args.profile)
# The IAM boto3 client
iam_client = session.client('iam', region_name=args.region)


def get_attached_policy(policy_arn):
    """This function returns the attached policy document"""
    # Need to use list_policy_versions first to get the default version
    version_response = iam_client.list_policy_versions(PolicyArn=policy_arn)
    policy_document = None
    policy_version = "v1"
    # DEBUGGING
    if args.debug:
        pp.pprint({"policy_arn": policy_arn, "version_response": version_response})
    if version_response:
        for version in version_response['Versions']:
            if version['IsDefaultVersion']:
                # The default version is the one we want
                policy_version = version['VersionId']
                # DEBUGGING
                if args.debug:
                    pp.pprint({"Found Default Policy Version": policy_version})
                break
    # If for some reason there is no default then just try the policy ARN with "v1" as the version and see what happens
    get_policy_response = iam_client.get_policy_version(PolicyArn=policy_arn, VersionId=policy_version)
    # DEBUGGING
    if args.debug:
        pp.pprint({"policy_arn": policy_arn, "get_policy_response": get_policy_response})
    if get_policy_response:
        policy_document = get_policy_response['PolicyVersion']['Document']['Statement']

    return policy_document


def get_inline_policy(role_name, policy_name):
    """This function returns the inline policy document"""
    policy_response = iam_client.get_role_policy(RoleName=role_name, PolicyName=policy_name)
    # DEBUGGING
    if args.debug:
        pp.pprint({"role_name": role_name, "policy_name": policy_name,
                   "get_inline_policies() policy_response": policy_response})
    if policy_response['PolicyDocument']:
        return policy_response['PolicyDocument']['Statement']
    else:
        return None


def get_policy_details(iam_role_name):
    """This function handles retrieving IAM policy permissions. Policies can be either inline or attached and they
       are retrieved using totally different methods so the get_attached_policies() and get_inline_policies()
       methods are used to gather those details"""
    iam_role_policies = dict()
    # Get the list or resources policies, if any
    attached_response = iam_client.list_attached_role_policies(RoleName=iam_role_name)
    # DEBUGGING
    if args.debug:
        pp.pprint({"attached_response": attached_response})
    for attached_policy in attached_response['AttachedPolicies']:
        attached_policy_name = attached_policy['PolicyName']
        policy_arn = attached_policy['PolicyArn']
        iam_role_policies[attached_policy_name] = get_attached_policy(policy_arn)

    # Get the inline role policies, if any
    inline_response = iam_client.list_role_policies(RoleName=iam_role_name)
    # DEBUGGING
    if args.debug:
        pp.pprint({"inline_response": inline_response})
    if inline_response['PolicyNames']:
        for inline_policy_name in inline_response['PolicyNames']:
            iam_role_policies[inline_policy_name] = get_inline_policy(iam_role_name, inline_policy_name)

    return iam_role_policies


def iam_auditor():
    """This function handles printing IAM roles and associated policy details"""
    try:
        output_list = list()
        output_dict = dict()
        headers = ["Role", "Policy Details (What CAN Be Accessed)", "API Activity (What's ACTUALLY Being Accessed)"]
        # The config for the paginator, limit to only 10 results unless in verbose mode
        pagination_config = {'PageSize': 100} if args.verbose else {'PageSize': 10, 'MaxItems': 10}
        # Use a paginator since the AWS API defaults results to 50, with a max of 100
        iam_paginator = iam_client.get_paginator('list_roles')
        # The pagination iterator, will either be all IAM roles, or just 10 depending on verbosity
        iam_page_iterator = iam_paginator.paginate(PaginationConfig=pagination_config)
        # Filter only IAM Roles that have a last used date within the past 'x' amount of time
        iam_filtered_iterator = iam_page_iterator.search(f"Roles[] | [?RoleLastUsed.LastUsedDate != ``]")

        for iam_role in iam_filtered_iterator:
            iam_role_name = iam_role['RoleName']
            iam_role_policies = get_policy_details(iam_role_name)
            # DEBUGGING
            if args.debug:
                pp.pprint({"IAM Role Name": iam_role_name, "iam_role_policies": iam_role_policies})

            # Add the IAM Role to the output list
            output_list.append([iam_role_name, pp.pformat(iam_role_policies), ""])
            # Also add the IAM Role to the output dictionary
            output_dict[iam_role_name] = iam_role_policies

        # Just for the hell of it, save the results in a json file
        with open('iam_audit_results.json', 'w') as file_handler:
            json.dump(output_dict, file_handler)

        # If not in debug mode print the IAM audit results
        if not args.debug:
            print("\n*************************************************************************************************")
            print(tabulate(output_list, headers, tablefmt="grid"))
            if not output_list:
                print("NO AWS IAM ROLES WERE FOUND!")
    except ClientError as ce:
        print(f"ERROR! ClientError: {ce}")


if __name__ == '__main__':
    """The Main function"""
    print(f"Checking The AWS Account For {args.profile} In Region {args.region} . . . ")
    iam_auditor()
