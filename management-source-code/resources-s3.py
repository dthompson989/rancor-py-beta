#!usr/bin/python
"""View and Deploy websites with AWS"""
from pathlib import Path
import mimetypes
import click
import boto3
from botocore.exceptions import ClientError

# Python user: rancor-python
session = boto3.Session(profile_name='rancor-python')
s3 = boto3.resource('s3')


def push_website_content(bucket, path, key):
    content_type = mimetypes.guess_type(key)[0] or 'text/plain'
    bucket.upload_file(path, key, ExtraArgs={'ContentType': content_type})
    return


# Setup CLI commands and params
@click.group()
def cli():
    """Automating AWS"""
    pass


# List all S3 Buckets
@cli.command('list-buckets')
def list_buckets():
    """List All S3 Buckets"""
    for bucket in s3.buckets.all():
        print(bucket)


# List the contents of a specific S3 Bucket
@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List the contents of an S3 bucket"""
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)


# Create a new S3 bucket
@cli.command('create-bucket')
@click.argument('bucket')
@click.option('--public/--private', default=True)
@click.option('--website', is_flag=True)
def create_bucket(bucket, public, website):
    """Create and configure an S3 bucket"""
    s3_bucket = None
    try:
        s3_bucket = s3.create_bucket(
            Bucket=bucket,
            CreateBucketConfiguration={'LocationConstraint': session.region_name}
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            s3_bucket = s3.Bucket(bucket)
        else:
            raise e

    if public:
        policy = """{
            "Version":"2012-10-17",
	        "Statement":[{
                "Sid":"PublicReadGetObject",
	            "Effect":"Allow",
	            "Principal": "*",
	            "Action":["s3:GetObject"],
	            "Resource":["arn:aws:s3:::%s/*"]
	        }]
        }""" % s3_bucket.name

        policy = policy.strip()

        pol = s3_bucket.Policy()
        pol.put(Policy=policy)

    if website:
        ws = s3_bucket.Website()
        ws.put(WebsiteConfiguration={
            'ErrorDocument': {'Key': 'error.html'},
            'IndexDocument': {'Suffix': 'index.html'}
        })

    return


@cli.command('code-sync')
@click.argument('path', type=click.Path(exists=True))
@click.argument('bucket')
def code_sync(path, bucket):
    """Push code changes from local repo to AWS S3"""
    s3_bucket = s3.Bucket(bucket)

    # pathlib is used to handle differences in unix/linux/windows file systems
    root = Path(path).expanduser().resolve()
    print('Syncing {} to AWS S3 Bucket {} . . . '.format(path, bucket))

    # Recursive function to traverse through a directory and
    def handle_directory(target):
        for p in target.iterdir():
            if p.is_dir():
                handle_directory(p)
            if p.is_file():
                push_website_content(s3_bucket, str(p), str(p.relative_to(root)))

    handle_directory(root)
    print('Code Sync Complete!')


if __name__ == '__main__':
    cli()

# todo: polish up readme file; finish up cmd help doc