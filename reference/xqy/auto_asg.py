#!usr/bin/python3.7
import boto3
import pprint
import time
from botocore.exceptions import ClientError

# AWS Region
REGION = "us-east-1"
# Set the Boto3 session
SESSION = boto3.Session(profile_name="product-newlexis-dev")
# The IAM boto3 client
IAM_CLIENT = SESSION.client('autoscaling', region_name=REGION)
# The E Node and D Node ASG's
ASG_DICT = {'E_NODE_ASG': 'marklogic-shepards-creds-Delivery-Enodes-asg2019112014534857340000000a',
            'D_NODE_ASG': 'marklogic-shepards-creds-generic-dnode-us-east-1a-01-asg20191120145348289800000008'}
# Use a pretty printer for better printing
PP = pprint.PrettyPrinter()
# Debugging
DEBUG = True
# Scaling Variables (I don't like using magic numbers in a function call
SCALE_UP = 1
SCALE_DOWN = 0


def asg_scale(asg, capacity):
    """This function handles scaling the ASG's up or down"""
    try:
        scaling_response = IAM_CLIENT.update_auto_scaling_group(AutoScalingGroupName=asg, MinSize=capacity,
                                                                MaxSize=capacity, DesiredCapacity=capacity)
        if DEBUG:
            PP.pprint(scaling_response)
    except ClientError as ce:
        print(f"ERROR! ClientError: {ce}")


def auto_asg():
    """This is the function that checks if the ASG's exist and then figures out if we need to scale up or down,
       and which ASG needs to go first"""
    try:
        # Get the E Node and D Node ASG details
        asg_response = IAM_CLIENT.describe_auto_scaling_groups(AutoScalingGroupNames=[ASG_DICT['E_NODE_ASG'],
                                                                                      ASG_DICT['D_NODE_ASG']])
        if asg_response and asg_response['AutoScalingGroups'] and len(asg_response['AutoScalingGroups']) == 2:
            if DEBUG:
                print(f"asg_response:\n{PP.pformat(asg_response)}")

            # Both desired capacities are 0, scale up
            if asg_response['AutoScalingGroups'][0]['DesiredCapacity'] == 0 \
                    and asg_response['AutoScalingGroups'][1]['DesiredCapacity'] == 0:
                # D Node needs to scale up first, otherwise the E Node freaks out
                asg_scale(ASG_DICT['D_NODE_ASG'], SCALE_UP)
                # Sleep for 5 seconds, may not matter but lets try this out for now
                time.sleep(5)
                asg_scale(ASG_DICT['E_NODE_ASG'], SCALE_UP)
                print(f"\nScaling MarkLogic ASG's UP . . . ")

            # else scale down
            else:
                if DEBUG and (asg_response['AutoScalingGroups'][0]['DesiredCapacity'] == 0
                              or asg_response['AutoScalingGroups'][1]['DesiredCapacity'] == 0):
                    # We have some weird mixed situation, so just scale down to clean up and run script again if needed
                    print(f"\nWARNING!!! ASG's Are in a weird mixed scenario\n")
                print(f"\nScaling MarkLogic ASG's DOWN . . . ")
                # E Node needs to scale down first, otherwise the E Node freaks out . . . again
                asg_scale(ASG_DICT['E_NODE_ASG'], SCALE_DOWN)
                # Sleep for 5 seconds, may not matter but lets try this out for now
                time.sleep(5)
                asg_scale(ASG_DICT['D_NODE_ASG'], SCALE_DOWN)
        else:
            print(f"ERROR! ASG's DO NOT EXIST! YOU NEED TO TAKE A LOOK AT WHAT'S GOING ON")
            if DEBUG:
                print(f"Number of ASG's Found: {len(asg_response['AutoScalingGroups'])}\n"
                      f"RESPONSE:\n{PP.pformat(asg_response)}")
    except ClientError as ce:
        print(f"ERROR! ClientError: {ce}")


if __name__ == '__main__':
    """The Main function"""
    auto_asg()
