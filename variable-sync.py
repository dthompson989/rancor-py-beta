#!usr/bin/python
""" This is a script that pushes or pulls a list of files. The files and sub folder don't have to
    exist when pushing, it will be created by S3. The reason for this is I want to save tfvars and deployment config
    files in AWS S3 so I can switch between different computers and not have to copy and paste variables as they
    change (Plus I don't want some things in source control). """
import click
import boto3
from botocore.exceptions import ClientError
from pathlib import Path


# The boto3 session resource
S3 = boto3.resource('s3')
# The terraform file name tp upload/download
NAMES = ["terraform.tfvars", "deploy.json"]
# The AWS S3 bucket name to push to and pull from
BUCKET_ROOT = "rancor-terraform-backend"
# The only acceptable project argument names
PROJECT_LIST = ['terraform-jenkins',
                'terraform-lambda-ami',
                'terraform-projects-reference',
                'terraform-sns',
                'terraform-jenkins-iam',
                'terraform-auditor',
                'terraform-housekeeper-lambda',
                'pipeline.sh']


# Setup CLI commands and params
@click.group()
def cli():
    """Example: bash-3.2$ python3 variable-sync.py push terraform-jenkins"""
    pass


@cli.command('push')
@click.argument('project', type=click.Choice(PROJECT_LIST))
def push(project):
    """ Pushes a list of files to AWS S3 and replaces them. """
    if project == 'pipeline.sh':
        print(f"Pushing {project} file to AWS S3")
        path = Path.cwd().joinpath(project)
        try:
            response = S3.meta.client.upload_file(str(path),
                                                  BUCKET_ROOT,
                                                  str(project),
                                                  ExtraArgs={'ContentType': 'text/plain'})
            print("Push complete: {}".format(response))
        except ClientError as e:
            print("ClientError! {}".format(e))
    else:
        for name in NAMES:
            print(f"Pushing {project} {name} file to AWS S3")
            path = Path.cwd().joinpath(project).joinpath(name)
            try:
                response = S3.meta.client.upload_file(str(path),
                                                      BUCKET_ROOT,
                                                      str(project + '/' + name),
                                                      ExtraArgs={'ContentType': 'text/plain'})
                print("Push complete: {}".format(response))
            except ClientError as e:
                print("ClientError! {}".format(e))


@cli.command('pull')
@click.argument('project', type=click.Choice(PROJECT_LIST))
def pull(project):
    """ Pulls a list of files from AWS S3 and replaces them locally. """
    if project == 'pipeline.sh':
        print(f"Pulling {project} file from AWS S3")
        path = Path.cwd().joinpath(project)
        try:
            response = S3.meta.client.download_file(BUCKET_ROOT,
                                                    str(project),
                                                    str(path))
            print("Pull complete: {}".format(response))
        except ClientError as e:
            print("ClientError! {}".format(e))
    else:
        for name in NAMES:
            print(f"Pulling {project} {name} file from AWS S3")
            path = Path.cwd().joinpath(project).joinpath(name)
            try:
                response = S3.meta.client.download_file(BUCKET_ROOT,
                                                        str(project + '/' + name),
                                                        str(path))
                print("Pull complete: {}".format(response))
            except ClientError as e:
                print("ClientError! {}".format(e))


if __name__ == '__main__':
    cli()
