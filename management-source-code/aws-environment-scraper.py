#!usr/bin/python
""" **** AWS TEMPLATE ****

   This set of functions are used to gather detailed information about AWS environment using boto3, save it to an html
   file, and push the file to AWS S3. *Note: It may not really save the file locally

   The first iteration will be this function, however the end goal will be to have an AWS Lambda function do this,
   possible on a schedule or something, so it runs itself weekly"""
import boto3

# A dictionary of all the tags I want to search for
TAG_DICT = {'tag:Type': 'EC2'}
# The chunk size of file parts to upload to S3
CHUNK_SIZE = 8388608
# The AWS S3 bucket to load file(s) to
S3_BUCKET = 'rancor-us-east-virginia'

ec2_client = boto3.client('ec2')


# List the ec2 instances based on tag name and value
def get_instances(tag_name, tag_value):
    """List EC2 Instances using tags for filtering"""
    obj = ec2_client.describe_instances(Filters=[{'Name': tag_name, 'Values': [tag_value]}])

    for reservation in obj["Reservations"]:
        for instance in reservation["Instances"]:
            print("Instance ID: " + instance["InstanceId"])
            print("Instance Type: " + instance["InstanceType"])
            print("AMI: " + instance["ImageId"])
            print("VPC: " + instance["VpcId"])
            print("Subnet: " + instance["SubnetId"])
            print("Availability Zone: " + instance["Placement"]["AvailabilityZone"])
            print("Security Groups: ")
            for sec_group in instance["SecurityGroups"]:
                print("    - " + sec_group["GroupName"])
            print("Machine State: " + instance["State"]["Name"])
            print("Root Name: " + instance["RootDeviceName"])
            print("Root Type: " + instance["RootDeviceType"])
            print("EBS Optimized: {}".format(instance["EbsOptimized"]))
            print("Volumes: ")
            for vol in instance["BlockDeviceMappings"]:
                print("    - Path: " + vol["DeviceName"])
                print("    - ID: " + vol["Ebs"]["VolumeId"])


# The master control flow function
def master_scraper():
    """The master scraper function. Calls the other functions"""
    for tag_name, tag_value in TAG_DICT.items():
        get_instances(tag_name, tag_value)


if __name__ == '__main__':
    master_scraper()
