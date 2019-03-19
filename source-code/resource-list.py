# Using Boto3 to interact with AWS
import boto3

# Python user: rancor-python
session = boto3.Session(profile_name='rancor-python')


# Beta function it list AWS EC2 instances
def list_instances():
    ec2 = session.resource('ec2')

    print('EC2:')

    for i in ec2.instances.all():
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name if i.public_dns_name else 'None')))

    return


''' 
    The basic design flow should be:
    1: main function
    2: function to check resource state
    3: function to get instances
    4: function to start/stop instances
    
    * EC2, DynamoDB, S3, RDS, Lambda, SNS, Glacier
    
    IDEAS:
        - Automatically create entire AWS environment (ie create anything that doesn't already exist)
'''

if __name__ == '__main__':
    list_instances()
