#!usr/bin/python
"""View and Create S3 buckets and Deploy websites to S3 with click and boto3"""
import click
import boto3
from s3class import S3Manager


# Python user: rancor-python
session = boto3.Session(profile_name='rancor-python')
s3_bucket = S3Manager(session)


# Setup CLI commands and params
@click.group()
def cli():
    """Setting up command line tool"""
    pass


# List all S3 Buckets
@cli.command('list-buckets')
def list_buckets():
    """List All S3 Buckets"""
    for bucket in s3_bucket.all_buckets():
        print(bucket)


# List the contents of a specific S3 Bucket
@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List the contents of an S3 bucket"""
    for obj in s3_bucket.all_objects(bucket):
        print(obj)


# Create a new S3 bucket
@cli.command('create-bucket')
@click.argument('bucket')
@click.option('--public/--private', default=True)
@click.option('--website', is_flag=True)
def create_bucket(bucket, public, website):
    """Create and configure an S3 bucket"""
    new_bucket = s3_bucket.create_bucket(bucket)
    if public:
        s3_bucket.set_policy(new_bucket)
    if website:
        s3_bucket.config_website(new_bucket)


# Command from pipenv shell:
#     python management-source-code/resources-s3.py code-sync david-m-thompson-website/ david-m-thompson-website
@cli.command('code-sync')
@click.argument('path', type=click.Path(exists=True))
@click.argument('bucket')
def code_sync(path, bucket):
    """Push code changes from local repo to AWS S3"""
    s3_bucket.code_sync(path, bucket)


if __name__ == '__main__':
    cli()

# todo: polish up readme file; finish up cmd help doc
