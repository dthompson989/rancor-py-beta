#!usr/bin/python3
"""This Lambda is an EC2 auditor Lambda. It is in charge of ensuring EC2 instances are compliant"""
import os
import boto3
from botocore.exceptions import ClientError

ec2_client = boto3.client('ec2')


def list_instances(tag_name, tag_value):
    """List EC2 Instances using the 'Name' tag for filtering"""
    try:
        obj = ec2_client.describe_instances(Filters=[{'Name': tag_name, 'Values': [tag_value]}])
        return obj
    except ClientError as e:
        print("ERROR! from list_instances() {}".format(e))
        return False


def auditor(event, context):
    """The Main Handler"""
    print(event)
    name = "rancor-jenkins"
    try:
        obj = list_instances("Name", name)
        if obj:
            for reservation in obj["Reservations"]:
                for instance in reservation["Instances"]:
                    ec2_id = instance["InstanceId"]
                    print(ec2_id)
        else:
            print("WARNING! There is no {} ec2 instance found!".format(name))
    except ClientError as e:
        print("ERROR! from auditor() {}".format(e))

# Use pytest and/or botocore.stub for testing
