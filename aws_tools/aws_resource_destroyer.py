#!usr/bin/python3.7
"""Usage: python3 aws_resource_destroyer.py -h """
import argparse
import boto3
import pprint
from botocore.exceptions import ClientError

# The list of acceptable services
service_list = ['ec2', 'lambda', 'cloudformation', 'rds']
# Parser for command line arguments
parser = argparse.ArgumentParser(prog="python3 aws_resource_destroyer.py",
                                 description="This is a script that will delete an AWS resource in the provided "
                                             "account, region, and service. Currently, the only services supported "
                                             "are ec2, lambda, and cloudformation, but more are on the way. "
                                             "Alternatively you can clone and modify the source code to suit your "
                                             "needs. For ec2, you can provide a comma separated list")
# Add parser arguments
parser.add_argument("-p",
                    "--profile",
                    dest="profile",
                    required=True,
                    help="REQUIRED. The AWS profile name to use")
parser.add_argument("-resource",
                    "--resource",
                    dest="resource",
                    required=True,
                    help="REQUIRED. The AWS resource ID to delete. Example: i-0100d0000f000fb00")
parser.add_argument("-s",
                    "--service",
                    dest="service",
                    required=True,
                    choices=service_list,
                    help="REQUIRED. The AWS service you are deleting from. Example: ec2")
parser.add_argument("-r",
                    "--region",
                    dest="region",
                    required=False,
                    default="us-east-1",
                    help="The AWS region to check. Default is us-east-1")
parser.add_argument("-d",
                    "--debug",
                    dest="debug",
                    action="store_true",
                    default=False,
                    help="The AWS region to check. Default is us-east-1")
# TODO: Change this to accept a single instance or a list to delete.
# Parse the arguments
args = parser.parse_args()
# If in debug mode, then use the pretty printer for output
if args.debug:
    pp = pprint.PrettyPrinter()

# Set the Boto3 session
session = boto3.Session(profile_name=args.profile)
# The Boto3 client
client = session.client(args.service, region_name=args.region)


def destroyer(checker=True):
    """This function handles the deleting of ec2 resource(s)"""
    try:
        # Perform a dry run first using checker = True, if checker = False then terminate the resource
        if args.service == 'ec2':
            response = client.terminate_instances(InstanceIds=[args.resource], DryRun=checker)
        elif args.service == 'lambda':
            if checker:
                response = client.get_function(FunctionName=args.resource)
            else:
                response = client.delete_function(FunctionName=args.resource)
        elif args.service == 'rds':
            if checker:
                response = client.describe_db_instances(DBInstanceIdentifier=args.resource)
            else:
                response = client.delete_db_instance(DBInstanceIdentifier=args.resource,
                                                     SkipFinalSnapshot=False,
                                                     DeleteAutomatedBackups=False)
        elif args.service == 'cloudformation':
            if checker:
                response = client.describe_stacks(StackName=args.resource)
            else:
                response = client.delete_stack(StackName=args.resource)
        else:
            return False

        if args.debug:
            pp.pprint(response)
        if response:
            return True
    except ClientError as ce:
        # During an ec2 dry run operation, the response is actually a thrown error. A success will have both
        # of the below key words in the error message
        go_list = ["DryRunOperation", "succeeded"]
        if all(i in str(ce) for i in go_list):
            if args.debug:
                print(f"ALL GOOD SO FAR! {ce}")
            return True
        else:
            if args.debug:
                print(f"ERROR! ClientError: {ce}")
            elif checker:
                print("ERROR! There was an error while checking to see if you can delete. "
                      "Use the '-d' flag to debug \n")
            else:
                print("ERROR! There was an error while trying to delete. Use the '-d' flag to debug \n")
    return False


if __name__ == '__main__':
    """The Main function"""
    print(f"\nChecking The AWS Account For {args.profile} In Region {args.region} . . .")
    print(f"{args.resource} belongs to {args.service}\n")
    can_delete = destroyer()
    if can_delete:
        if "prod" in args.profile:
            print(f"********************************************")
            print(f"WARNING!!! THIS IS A PRODUCTION ENVIRONMENT!\n")
        proceed = input(f"You are about to delete/terminate live AWS resources . . . \n"
                        f"ARE YOU SURE YOU WANT TO CONTINUE? (Y/n) ")
        if proceed.upper() == 'Y':
            is_destroyed = destroyer(False)
            if is_destroyed:
                print("All done! Have a nice day.")
        else:
            print("Okay, so we are not deleting anything right now . . . \nMaybe some other time then. Goodbye . . . ")
