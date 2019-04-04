#!usr/bin/python
"""View and Create S3 buckets and Deploy websites to S3 with click and boto3"""
import click
import boto3
from ec2class import EC2Manager


# Python user: rancor-python
session = boto3.Session(profile_name='rancor-python')
ec2_object = EC2Manager(session)


# Setup CLI commands and params
@click.group()
def cli():
    """Setting up command line tool"""
    pass


# List all EC2 Instances
@cli.command('list-instances')
def list_buckets():
    """List All EC2 Instances"""
    for i in ec2_object.all_instances():
        print(i)


# List the contents of a specific S3 Bucket
@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List the contents of an S3 bucket"""
    for obj in ec2_object.all_objects(bucket):
        print(obj)


if __name__ == '__main__':
    cli()

# todo: polish up readme file; finish up cmd help doc