#!usr/bin/python3.7
import os
import logging
import boto3
from botocore.exceptions import ClientError

# Configure the logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# The SSM boto3 Client
ssm_client = boto3.client('ssm')
# Lambda Environment Variables
DOCUMENT_NAME = os.environ['DOCUMENT_NAME']


def manager(event, context):
    """ The Main Handler
    :param event: The event object from CloudWatch (CRON job)
    :param context: The context (Not used)
    :return: None (SNS Topic is sent results)
    """
    logger.info(f"INFO! ssm manager event started: event: {event}")
    try:
        # Use a paginator since the AWS API defaults results to 1 page, with a max of 50
        ssm_inventory_paginator = ssm_client.get_paginator('get_inventory')
        ssm_inventory_page_iterator = ssm_inventory_paginator.paginate(PaginationConfig={'PageSize': 50},
                                                                       InstanceInformationFilter=[
                                                                           {
                                                                               'key': 'PingStatus',
                                                                               'valueSet': ['Online']
                                                                           }, {
                                                                               'key': 'PlatformTypes',
                                                                               'valueSet': ['Linux']
                                                                           }
                                                                       ])

        for pages in ssm_inventory_page_iterator:
            instance_list = []
            for instance in pages['InstanceInformationList']:
                instance_list.append(instance['InstanceId'])
            automation_response = ssm_client.start_automation_execution(DocumentName=DOCUMENT_NAME,
                                                                        Parameters={'ec2InstanceIds': instance_list},
                                                                        MaxConcurrency='50%',
                                                                        MaxErrors='100%')
            logger.info(f"INFO! ssm start_automation_execution ::: instance_list: {instance_list} ::: "
                        f"response: {automation_response}")
            if not automation_response:
                logger.error(f"ERROR! Response Error!")

    except ClientError as ce:
        logger.error(f"ERROR! ClientError: {ce}")
