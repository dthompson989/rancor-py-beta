#!usr/bin/python3.7
""" This Lambda is a housekeeping Lambda. It is in charge of checking for expiring certificates, and in the future,
    other things as well. """
import datetime
import json
import logging
import boto3
from botocore.exceptions import ClientError

# Configure the logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Global constants
POST_TO_SLACK_LAMBDA = "rancor-slack-dev-post-to-slack"


def post_to_slack(notification_list):
    """ This is a helper function that invokes the rancor-slack-dev-post-to-slack Lambda function. """
    logger.debug(f"DEBUG! post_to_slack starting . . . ")
    try:
        payload = {"Records": [{
            "LambdaEvent": "Lambda",
            "Subject": "Housekeeper Lambda Report",
            "Message": ",".join(notification_list)
        }]}
        lambda_client = boto3.client('lambda', region_name='us-east-1')
        lambda_response = lambda_client.invoke(FunctionName=POST_TO_SLACK_LAMBDA,
                                               InvocationType='Event',
                                               Payload=json.dumps(payload))
        if lambda_response['StatusCode'] == 202:
            logger.info(f"INFO! post_to_slack lambda_response SUCCESS: {lambda_response}")
        else:
            logger.error(f"ERROR! post_to_slack lambda_response FAILURE: {lambda_response}")
    except ClientError as ce:
        logger.error(f"ERROR! post_to_slack ClientError: {ce}")


def check_certs():
    """ This is a helper function that lists certs, gets their details, and checks to see is any are expiring within
        60 days. """
    expiring_certs_list = []
    logger.debug(f"DEBUG! check_certs starting . . . ")
    try:
        acm_client = boto3.client("acm", "us-east-1")
        logger.debug(f"DEBUG! check_certs acm_client created . . . ")
        list_response = acm_client.list_certificates()
        logger.debug(f"DEBUG! check_certs list_response: {list_response}")
        try:
            for cert in list_response['CertificateSummaryList']:
                cert_arn = cert['CertificateArn']
                domain = cert['DomainName']
                logger.info(f"INFO! check_certs domain: {domain} ::: cert_arn: {cert_arn}")
                describe_cert_response = acm_client.describe_certificate(CertificateArn=cert_arn)
                logger.debug(f"DEBUG! check_certs describe_cert_response: {describe_cert_response}")
                try:
                    sixty_days = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=60)
                    expiration_date = describe_cert_response['Certificate']['NotAfter']
                    logger.info(f"INFO! check_certs {domain} cert expires {expiration_date}")
                    if expiration_date < sixty_days:
                        logger.debug(f"DEBUG! check_certs adding {cert_arn} for {domain} to expiring_certs_list")
                        expiring_certs_list.append(f"Certificate for Domain {domain} is set to expire "
                                                   f"{expiration_date.strftime('%m-%d-%y')}")
                    else:
                        logger.debug(f"DEBUG! check_certs cert_arn: {cert_arn} ::: expiration_date comparison: "
                                     f"{expiration_date}>{sixty_days}")
                except IndexError as ie:
                    logger.error(f"ERROR! check_certs describe_cert_response = acm_client.describe_certificate() "
                                 f"IndexError: {ie}")
        except IndexError as ie:
            logger.error(f"ERROR! check_certs list_response=acm_client.list_certificates() IndexError: {ie}")

    except ClientError as ce:
        logger.error(f"ERROR! check_certs ClientError: {ce}")

    return expiring_certs_list


def main(event, context):
    """ The Main Handler - Used to perform basic housekeeping of AWS environment including checking for expiring
                           certificates.
        :param event: The event object from CloudWatch CRON
        :param context: The context (Not used)
        :return: None
        Author: David Thompson
        Version: 1.0
    """
    logger.info(f"INFO! Starting housekeeper . . . ")
    logger.debug(f"DEBUG! main event: {event} ::: context: {context}")
    try:
        # Check for certificates expiring in the near future
        certs = check_certs()
        if certs:
            logger.debug(f"DEBUG! main check_certs() certs: {certs}")
            post_to_slack(certs)
        else:
            post_to_slack(["No Housekeeping Needed"])
            logger.info(f"INFO! There are no certificates expiring soon")
    except ClientError as ce:
        logger.error(f"ERROR! main ClientError {ce}")
