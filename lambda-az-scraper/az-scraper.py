#!usr/bin/python
"""View detailed information about EC2 Instances with click and boto3"""
import boto3

ec2_client = boto3.client('ec2')
s3_client = boto3.client('s3')


def get_regions():
    """A function to gather the regions"""


def handler(event, context):
    """The main function for an AWS Lambda function"""
