#!usr/bin/python
"""View detailed information about EC2 Instances with click and boto3"""
import click
import boto3

ec2_client = boto3.client('ec2')


# Setup CLI commands and params
@click.group()
def cli():
    """Setting up command line tool"""
    pass


# List the contents of a specific S3 Bucket
@cli.command('list-instance')
@click.argument('tag-name')
@click.argument('tag-value')
def list_instance(tag_name, tag_value):
    """List EC2 Instances using tags for filtering"""
    obj = ec2_client.describe_instances(Filters=[{'Name': tag_name, 'Values': [tag_value]}])

    for reservation in obj["Reservations"]:
        for instance in reservation["Instances"]:
            print("-------------------------------------")
            print("Instance ID: " + instance["InstanceId"])
            print("Instance Type: " + instance["InstanceType"])
            print("AMI: " + instance["ImageId"])
            print("VPC: " + instance["VpcId"])
            print("Subnet: " + instance["SubnetId"])
            print("Availability Zone: " + instance["Placement"]["AvailabilityZone"])
            print("Security Groups: ")
            for sec_group in instance["SecurityGroups"]:
                print("    - " + sec_group["GroupName"])
            print("Root Name: " + instance["RootDeviceName"])
            print("Root Type: " + instance["RootDeviceType"])
            print("EBS Optimized: {}".format(instance["EbsOptimized"]))
            print("Volumes: ")
            for vol in instance["BlockDeviceMappings"]:
                print("    - Path: " + vol["DeviceName"])
                print("    - ID: " + vol["Ebs"]["VolumeId"])
    print("-------------------------------------")


if __name__ == '__main__':
    cli()

# todo: polish up readme file; finish up cmd help doc
