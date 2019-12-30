#!usr/bin/python
"""View EC2 Instances Availability Zone break down using boto3"""
import boto3

ec2_client = boto3.client('ec2')
s3_client = boto3.client('s3')


def list_instances():
    """A function to describe the instances in a given region"""
    obj = ec2_client.describe_instances(Filters=[{'Name': 'instance-state-name',
                                                  'Values': ['pending', 'running', 'stopped']}])

    for reservation in obj["Reservations"]:
        for instance in reservation["Instances"]:
            print("{}: Availability Zone: {}".format(instance["InstanceId"], instance["Placement"]["AvailabilityZone"]))


def lambda_handler(event, context):
    """The main function for an AWS Lambda function"""
    list_instances()


if __name__ == '__main__':
    """Main function if running in the command line"""
    list_instances()
