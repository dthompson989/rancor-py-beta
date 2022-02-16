#!usr/bin/python
""" A Lambda function that receives events from AWS Services, Logs the event, and sends a notification to slack.
    Built using Serverless. Currently receives events from S3, SNS, & Lambda"""
import os
import requests
import logging
import json

# Configure the logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def post_to_slack(event, context):
    """The lambda handler function"""
    logger.info(f"INFO! Starting post to slack . . . ")
    logger.debug(f"DEBUG! post_to_slack event: {event} ::: context: {context}")
    slack_url = os.environ['SLACK_URL']

    """Try to post to slack, logging the successful or unsuccessful attempt"""
    try:
        """Convert json to a python object"""
        data = json.loads(str(event).replace("\'", "\""))
        source = 'ERROR'
        subject = 'ERROR'
        detail = 'ERROR'

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
            source = data['Records'][0]['LambdaEvent']
            subject = data['Records'][0]['Subject']
            detail = data['Records'][0]['Message']
        else:
            logger.error(f"ERROR! post_to_slack eventSource, EventSource, and LambdaEvent missing from event "
                         f"Record ::: {event}")

        # If the event that triggered this Lambda, for some reason has not been defined, I still want to know.
        slack_message = f"From {source} {subject} {detail}"
        data = {"text": slack_message}
        response = requests.post(slack_url, json=data)
        logger.info(f"INFO! post_to_slack {source} LAMBDA Success Response Code: {response.status_code}")
    except Exception as e:
        logger.error(f"ERROR! post_to_slack Exception: {e} ::: event {event}")
        return None

    return response.status_code
