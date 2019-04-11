#!usr/bin/python
"""This set of functions are used to gather detailed information about AWS environment using boto3, save it to an html
   file, and push the file to AWS S3. *Note: It may not really save the file locally

   The first iteration will be this function, however the end goal will be to have an AWS Lambda function do this,
   possible on a schedule ot something, so it runs itself weekly"""
import boto3

ec2_client = boto3.client('ec2')


# List the ec2 instances based on tag name and value
def list_instances(tag_name, tag_value):
    """List EC2 Instances using tags for filtering"""
    obj = ec2_client.describe_instances(Filters=[{'Name': tag_name, 'Values': [tag_value]}])

    for reservation in obj["Reservations"]:
        for instance in reservation["Instances"]:
            instance["InstanceId"]


# The master control flow function
def master_scraper():
    """The master scraper function. Calls the other functions"""


if __name__ == '__main__':
    master_scraper()
