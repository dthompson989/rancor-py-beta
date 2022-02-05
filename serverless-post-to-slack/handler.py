#!usr/bin/python
""" A Lambda function that receives events from AWS Services, Logs the event, and sends a notification to slack.
    Built using Serverless. Currently receives events from S3, SNS, & Lambda"""
import os
import requests
from requests.exceptions import HTTPError
import json


def post_to_slack(event, context):
    """The lambda handler function"""
    slack_url = os.environ['SLACK_URL']

    """Try to post to slack, logging the successful or unsuccessful attempt"""
    try:
        """Convert json to a python object"""
        data = json.loads(event)
        source = 'None'
        subject = 'None'
        detail = 'None'

        # Event from S3
        if 'eventSource' in data['Records'][0]:
            source = data['Records'][0]['eventSource']
            subject = data['Records'][0]['eventName']
            detail = data['Records'][0]['s3']['object']['key']
        # Event from SNS
        elif 'EventSource' in data['Records'][0]:
            source = data['Records'][0]['EventSource']
            subject = data['Records'][0]['Sns']['Subject']
            detail = data['Records'][0]['Sns']['Message']
        # Event from another Lambda Function
        elif 'LambdaEvent' in data['Records'][0]:
            source = data['Records'][0]['EventSource']
            subject = data['Records'][0]['Subject']
            detail = data['Records'][0]['Message']

        # If the event that triggered this Lambda, for some reason has not been defined, I still want to know.
        slack_message = "From {} {} {}".format(source, subject, detail)
        data = {"text": slack_message}
        response = requests.post(slack_url, json=data)
        print("{} LAMBDA Success Response Code: {}".format(source, response.status_code))
    except Exception as e:
        print("LAMBDA FAILED!!! Error: {} ::: Event {}".format(e, event))
        return None

    return response.status_code

# Use pytest and/or botocore.stub for testing
