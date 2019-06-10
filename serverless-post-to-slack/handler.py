#!usr/bin/python
"""A Lambda function that receives events from S3, Logs the event, and sends a notification to slack using serverless"""
import os
import requests


def post_to_slack(event, context):
    """The lambda handler function"""
    slack_url = os.environ['SLACK_URL']

    """Try to post to slack, logging the successful or unsuccessful attempt"""
    try:
        slack_message = "From {} {} {}".format(event['eventSource'], event['eventName'], event['object']['key'])
        data = {"text": slack_message}
        response = requests.post(slack_url, json=data)
        print("S3 LAMBDA Success Response Code: " + response.status_code)
    except Exception as e:
        print("S3 LAMBDA FAILED!!! Error: {} ::: Event {}".format(e, event))

    return
