# Using Boto3 to interact with AWS
import boto3
import click
from botocore.exceptions import ClientError

# Python user: rancor-python
session = boto3.Session(profile_name='rancor-python')


# Beta function it list AWS EC2 instances
def ec2_instances(opt):
    ec2 = session.resource('ec2')

    print('EC2:')
    if opt == 'list':
        for i in ec2.instances.all():
            print(', '.join((
                i.id,
                i.instance_type,
                i.placement['AvailabilityZone'],
                i.state['Name'],
                i.public_dns_name if i.public_dns_name else 'None')))
    elif opt == 'start':
        for i in ec2.instances.all():
            if i.state['Name'] == 'stopped':
                try:
                    ec2.start_instances(InstanceIds=[i.id], DryRun=False)
                    print('Starting {0} . . . '.format(i.id))
                except ClientError as e:
                    print(e)
    elif opt == 'stop':
        for i in ec2.instances.all():
            if i.state['Name'] == 'running':
                try:
                    ec2.stop_instances(InstanceIds=[i.id], DryRun=False)
                    print('Stopping {0} . . . '.format(i.id))
                except ClientError as e:
                    print(e)
    else:
        print('Bad input')

    return


if __name__ == '__main__':
    ec2_instances('list')


"""
    * EC2, DynamoDB, S3, RDS, Lambda, SNS, Glacier

    IDEAS:
        - CLoud formation template
        - Notify via slack
        
"""
