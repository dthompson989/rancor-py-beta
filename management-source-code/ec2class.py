"""AWS EC2 Instance Detailed List Class"""


class EC2Manager:
    """Manage EC2 Instances"""

    def __init__(self, session):
        """Create ec2 manager object"""
        self.session = session
        self.ec2 = self.session.resource('ec2')

    def list_instances(self, tag_name, tag_value):
        """Return a detailed list of EC2 instance(s)"""
        return self.ec2.describe_instances(Filters=[{'Name': tag_name, 'Values': [tag_value]}])
        # filter by TAG or Instance ID
