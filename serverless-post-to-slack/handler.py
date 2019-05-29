#!usr/bin/python
"""A Lambda function that receives events from S3, Logs the event, and sends a notification to slack using boto3"""
import os
import requests


def post_to_slack(event, context):
    """The lambda handler function"""
    slack_url = os.environ['SLACK_URL']
    slack_message = "From {source} at {detail[StartTime]}: {detail[Description]}".format(**event)
    data = {"text": slack_message}

    try:
        response = requests.post(slack_url, json=data)
        print(event + " Response Code: " + response.status_code)
    except Exception as e:
        print(event + " FAILED!!! {}".format(e))

    return
