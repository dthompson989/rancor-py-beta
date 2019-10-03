#!usr/bin/python3
"""This Lambda is an AMI maintenance Lambda. It is in charge of creating, deleting, and auditing AMI's"""
import boto3
from botocore.exceptions import ClientError

ec2_client = boto3.client('ec2')


def delete_images(ami_name):
    """De-registers any preexisting AMI(s) with the same name"""
    try:
        obj = ec2_client.describe_images(Filters=[{'Name': "Name", 'Values': [ami_name]}])
        if obj:
            for image in obj['Images']:
                image_id = image['ImageId']
                ec2_client.deregister_image(ImageId=image_id)
                print("INFO! De-registered {}".format(image_id))
        else:
            print("WARNING! There are no {} ami images found!".format(ami_name))
    except ClientError as e:
        print("ERROR! from delete_images() {}".format(e))


def create_image(ec2_id, ec2_name):
    """Controls the creation of an AMI image, given an ec2 instance ID"""
    if ec2_id and ec2_name:
        ami_name = ec2_name + "-ami"
        delete_images(ami_name)
        try:
            response = ec2_client.create_image(InstanceId=ec2_id, Description=ami_name, Name=ami_name)
            return response
        except ClientError as e:
            print("ERROR! from create_image() {}".format(e))
            return False
    else:
        print("ERROR! THERE IS NO ID AND NAME!")
        return False


def list_instances(tag_name, tag_value):
    """List EC2 Instances using the 'Name' tag for filtering"""
    try:
        obj = ec2_client.describe_instances(Filters=[{'Name': tag_name, 'Values': [tag_value]}])
        return obj
    except ClientError as e:
        print("ERROR! from list_instances() {}".format(e))
        return False


def auto_ami(event, context):
    """The Main Handler"""
    print(event)
    name = "rancor-jenkins"
    try:
        obj = list_instances("Name", name)
        if obj:
            for reservation in obj["Reservations"]:
                for instance in reservation["Instances"]:
                    ec2_id = instance["InstanceId"]
                    image = create_image(ec2_id, name)
                    if image:
                        print("Successfully create {} image ID: {}".format(name, image['ImageId']))
                    else:
                        print("ERROR! THERE WAS NO IMAGE CREATED!")
        else:
            print("WARNING! There is no {} ec2 instance found!".format(name))
    except ClientError as e:
        print("ERROR! from auto_ami() {}".format(e))
