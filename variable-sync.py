#!usr/bin/python
""" This is a script that pushes or pulls terraform.tfvars files. The file and sub folder don't have to
    exist when pushing, it will be created by S3. The reason for this is I want to save tfvars files in
    AWS S3 so I can switch between different computers and not have to copy and paste variables as they
    change. """
import click
import boto3
from botocore.exceptions import ClientError
from pathlib import Path


# The boto3 session resource
s3 = boto3.resource('s3')
# The terraform file name tp upload/download
NAME = "terraform.tfvars"
# The AWS S3 bucket name
BUCKET_ROOT = "rancor-terraform-backend"
# The only acceptable project argument names
PROJECT_LIST = ['terraform-jenkins',
                'terraform-lambda',
                'terraform-projects-reference',
                'terraform-sns',
                'terraform-jenkins-iam',
                'terraform-auditor']


# Setup CLI commands and params
@click.group()
def cli():
    """Example: bash-3.2$ python variable-sync.py push terraform-jenkins"""
    pass


@cli.command('push')
@click.argument('project', type=click.Choice(PROJECT_LIST))
def push(project):
    """Pushes a terraform.tfvars file to AWS S3 and replaces it"""
    print("Pushing {} terraform.tfvars file to AWS S3".format(project))
    path = Path.cwd().joinpath(project).joinpath(NAME)
    try:
        response = s3.meta.client.upload_file(str(path),
                                              BUCKET_ROOT,
                                              str(project + '/' + NAME),
                                              ExtraArgs={'ContentType': 'text/plain'})
        print("Push complete: {}".format(response))
    except ClientError as e:
        print("ClientError! {}".format(e))


@cli.command('pull')
@click.argument('project', type=click.Choice(PROJECT_LIST))
def pull(project):
    """Pulls a terraform.tfvars file from AWS S3 and replaces it"""
    print("Pulling {} terraform.tfvars file from AWS S3".format(project))
    path = Path.cwd().joinpath(project).joinpath(NAME)
    try:
        response = s3.meta.client.download_file(BUCKET_ROOT,
                                                str(project + '/' + NAME),
                                                str(path))
        print("Pull complete: {}".format(response))
    except ClientError as e:
        print("ClientError! {}".format(e))


if __name__ == '__main__':
    cli()
