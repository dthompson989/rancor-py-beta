#!usr/bin/python3.7
""" This is a tool that deploys a websites frontend (ie copies html, js, and css files to AWS S3). This script is
    called from pipeline.sh

    Usage: $ python3 website-deploy-tool.py -p <project> -e <environment> -d
    Example: $ python3 website-deploy-tool.py -p david-m-thompson-website -e dev
"""
import argparse
import boto3
import os
from botocore.exceptions import ClientError
from pathlib import Path

# The boto3 session resource
S3 = boto3.resource('s3', 'us-east-1')
ENV_CONFIG = {
    "dev": "dev.davidthompson.cloud",
    "prod": "davidthompson.cloud"
}
FILES_TO_UPLOAD_LIST = []
FILE_EXCLUSION_LIST = ["deploy.json", "README.md", ".DS_Store"]

# Parser for command line arguments
parser = argparse.ArgumentParser(prog="python3 website-deploy-tool.py",
                                 description="This is a tool that deploys a websites frontend (ie copies html, js, "
                                             "and css files to AWS S3)")
# Add parser arguments
parser.add_argument("-p",
                    "--project",
                    dest="project",
                    required=True,
                    help="REQUIRED. The directory or project to deploy. HINT: Enter the relative path to the target.")
parser.add_argument("-e",
                    "--environment",
                    dest="environment",
                    required=True,
                    help="REQUIRED. Deploy to DEV or PROD environment.")
parser.add_argument("-d",
                    "--debug",
                    dest="debug",
                    action="store_true",
                    default=False,
                    help="If set, turns on debugging. The default is False")
# Parse the arguments
args = parser.parse_args()


def copy_to_aws():
    """ A helper function that takes the FILES_TO_UPLOAD_LIST list and uploads them to AWS S3. """
    if args.debug:
        print(f"DEBUG! copy_to_aws beginning . . .")
    for file in FILES_TO_UPLOAD_LIST:
        if args.debug:
            print(f"DEBUG! copy_to_aws file {file} processing")
        try:
            response = S3.meta.client.upload_file(str(file['path']),
                                                  ENV_CONFIG[args.environment],
                                                  str(file['upload_name']))
            print("Push complete: {}".format(response))
        except ClientError as ce:
            print(f"ERROR! ClientError on file {file}: {ce}")


def get_upload_files():
    """ A helper function that adds local files to the FILES_TO_UPLOAD_LIST list. """
    if args.debug:
        print(f"DEBUG! get_upload_files beginning . . .")
    # Get list of files and folders in the project provided.
    for dp, dn, filenames in os.walk(args.project):
        if args.debug:
            print(f"DEBUG! get_upload_files filenames: {filenames}\ndp: {dp}\n")
        # Iterate through list of files in the current directory
        for file in filenames:
            if file not in FILE_EXCLUSION_LIST:
                file_path = Path.cwd().joinpath(dp).joinpath(file)
                if args.debug:
                    print(f"DEBUG! get_upload_files file {file} appended")
                # AWS S3 upload needs the full path to the file and an object key (including prefix).
                FILES_TO_UPLOAD_LIST.append({'path': f"{file_path}",
                                             'upload_name': f"{os.path.relpath(str(file_path), args.project)}"})
            elif args.debug:
                print(f"DEBUG! get_upload_files file {file} excluded")


if __name__ == '__main__':
    """ The Main Handler - Used to gather a list of local files, and upload them to an AWS S3 bucket.
    
        :return: None
        Author: David Thompson
        Version: 1.0
    """
    if args.debug:
        print(f"DEBUG! __main__ project: {args.project}\n\t environment: {args.environment}")
    get_upload_files()
    if FILES_TO_UPLOAD_LIST:
        if args.debug:
            print(f"DEBUG! __main__ FILES_TO_UPLOAD_LIST {FILES_TO_UPLOAD_LIST}")
        copy_to_aws()
    else:
        print(f"ERROR! __main__ FILES_TO_UPLOAD_LIST empty")
