# Using Boto3 to interact with AWS
import boto3
import click
from botocore.exceptions import ClientError

# Python user: rancor-python
session = boto3.Session(profile_name='rancor-python')
s3 = boto3.resource('s3')


# Setup CLI commands and params
@click.group()
def cli():
    """Automating AWS"""
    pass


@cli.command('list-buckets')
def list_buckets():
    """List All S3 Buckets"""
    for bucket in s3.buckets.all():
        print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List the contents of an S3 bucket"""
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)


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


if __name__ == '__main__':
    cli()
