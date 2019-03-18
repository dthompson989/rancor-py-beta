# Using Boto3 to interact with AWS
import boto3

# Python user: rancor-python
session = boto3.Session(profile_name='rancor-python')

ec2 = session.resource('ec2')

for i in ec2.instances.all():
    print(i)


# The basic design flow should be:
# 1: main function
# 2: function to check resource state
# 3: function to get instances
# 4: function to start/stop instances

