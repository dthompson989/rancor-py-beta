"""AWS EC2 Instance Detailed List Class"""
import boto3
from botocore.exceptions import ClientError
import util

class EC2Manager:
    """Manage EC2 Instances"""

    def __init__(self, session):
        """Create ec2 manager object"""
        self.session = session
        self.ec2 = self.session.resource('ec2')

    def show_instances(self, instance):
        """Return a detailed list of EC2 instance(s)"""
        return self.ec2.descibe_instances()
        # filter by TAG or Instance ID
