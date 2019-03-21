#!usr/bin/python
"""View and Deploy websites with AWS"""
import click
import boto3
from s3class import S3Manager


# Python user: rancor-python
session = boto3.Session(profile_name='rancor-python')
s3_bucket = S3Manager(session)


# Setup CLI commands and params
@click.group()
def cli():
    """Deploying to AWS"""
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

    print('Bucket Created: ' + new_bucket)


@cli.command('code-sync')
@click.argument('path', type=click.Path(exists=True))
@click.argument('bucket')
def code_sync(path, bucket):
    """Push code changes from local repo to AWS S3"""
    print('Syncing {} to AWS S3 Bucket {} . . . '.format(path, bucket))
    s3_bucket.code_sync(path, bucket)
    print('Code Sync Complete!')


if __name__ == '__main__':
    cli()

# todo: polish up readme file; finish up cmd help doc
