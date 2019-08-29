#!usr/bin/python
"""A Lambda function that receives events from AWS Services, Logs the event (in some way),
   and sends a notification to slack. Built using Serverless"""
import os
import requests


def post_to_slack(event, context):
    """The lambda handler function"""
    slack_url = os.environ['SLACK_URL']

    """Try to post to slack, logging the successful or unsuccessful attempt"""
    try:
        slack_message = "From {} {} {}".format(event['Records'][0]['eventSource'],
                                               event['Records'][0]['eventName'],
                                               event['Records'][0]['s3']['object']['key'])
        data = {"text": slack_message}
        response = requests.post(slack_url, json=data)
        print("S3 LAMBDA Success Response Code: {}".format(response.status_code))
    except Exception as e:
        print("S3 LAMBDA FAILED!!! Error: {} ::: Event {}".format(e, event))

    return
