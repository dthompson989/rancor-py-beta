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
HOUSEKEEPING_ISSUES = []


def post_to_slack(notification_list):
    """ This is a helper function that invokes the rancor-slack-dev-post-to-slack Lambda function.
        :param notification_list: A list of all the housekeeping issues found
        :return: None
    """
    logger.debug(f"DEBUG! post_to_slack starting . . . ")
    try:
        payload = {"Records": [{
            "LambdaEvent": "Lambda",
            "Subject": "Housekeeper Lambda Report",
            "Message": ",".join(notification_list)
        }]}
        logger.debug(f"DEBUG! post_to_slack payload: {payload}")
        lambda_client = boto3.client('lambda', region_name='us-east-1')
        logger.debug(f"DEBUG! post_to_slack lambda_client created")
        lambda_response = lambda_client.invoke(FunctionName=POST_TO_SLACK_LAMBDA,
                                               InvocationType='Event',
                                               Payload=json.dumps(payload))
        logger.debug(f"DEBUG! post_to_slack lambda_response: {lambda_response}")
        if lambda_response['StatusCode'] == 202:
            logger.info(f"INFO! post_to_slack lambda_response SUCCESS: {lambda_response}")
        else:
            logger.error(f"ERROR! post_to_slack lambda_response FAILURE: {lambda_response}")
    except ClientError as ce:
        logger.error(f"ERROR! post_to_slack ClientError: {ce}")


def check_rds(region_list):
    """ This is a helper function that checks for any RDS databases that have been created.
        :param region_list: A list of all available regions to check
        :return: None
    """
    logger.debug(f"DEBUG! check_rds starting . . .")
    for region in region_list:
        try:
            logger.debug(f"DEBUG! check_rds checking {region} region . . . ")
            rds_client = boto3.client("rds", region)
            logger.debug(f"DEBUG! check_rds {region} rds_client created . . .")
            rds_result = rds_client.describe_db_instances(MaxRecords=20)
            logger.debug(f"DEBUG! check_rds {region} rds_result: {rds_result}")
            try:
                if rds_result['DBInstances'] > 0:
                    logger.info(f"INFO! check_rds {region} databases found")
                    HOUSEKEEPING_ISSUES.append(f"RDS Database(s) found in {region}. IMMEDIATE ACTION NEEDED!")
                else:
                    logger.info(f"INFO! check_rds {region} databases NOT found")
            except KeyError as ke:
                logger.debug(f"DEBUG! check_rds KeyError: {ke}")
        except ClientError as ce:
            logger.error(f"ERROR! check_rds ClientError: {ce}")


def check_ec2(region_list):
    """ This is a helper function that checks for any EC2 instances that have been created.
        :param region_list: A list of all available regions to check
        :return: None
    """
    logger.debug(f"DEBUG! check_ec2 starting . . .")
    for region in region_list:
        try:
            logger.debug(f"DEBUG! check_ec2 checking {region} region . . . ")
            ec2_client = boto3.client("ec2", region)
            logger.debug(f"DEBUG! check_ec2 {region} ec2_client created . . .")
            ec2_result = ec2_client.describe_instances(MaxResults=5)
            logger.debug(f"DEBUG! check_ec2 {region} ec2_result: {ec2_result}")
            try:
                if ec2_result['Reservations'][0]['Instances'] > 0:
                    logger.info(f"INFO! check_ec2 {region} instances found")
                    HOUSEKEEPING_ISSUES.append(f"EC2 Instance(s) found in {region}. IMMEDIATE ACTION NEEDED!")
                else:
                    logger.info(f"INFO! check_ec2 {region} instances NOT found")
            except KeyError as ke:
                logger.debug(f"DEBUG! check_ec2 KeyError: {ke}")
        except ClientError as ce:
            logger.error(f"ERROR! check_ec2 ClientError: {ce}")


def get_regions():
    """ This is a helper function that returns a list of available regions for EC2 compute (and RDS as well).
        :return: region_list: A list of all available regions to check
    """
    logger.debug(f"DEBUG! get_regions starting . . . ")
    region_list = []
    try:
        client = boto3.client("ec2")
        logger.debug(f"DEBUG! get_regions client created . . .")
        region_list = [region['RegionName'] for region in client.describe_regions()['Regions']]
    except (ClientError, KeyError) as err:
        logger.error(f"ERROR! get_regions describe_regions exception: {err}")

    logger.debug(f"DEBUG! get_regions region_list: {region_list}")
    return region_list


def check_certs():
    """ This is a helper function that lists certs, gets their details, and checks to see is any are expiring within
        60 days.
        :return: None
    """
    logger.debug(f"DEBUG! check_certs starting . . . ")
    try:
        # Only checking us-east-1 certificates, I don't care about other regions at this time
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
                        HOUSEKEEPING_ISSUES.append(f"Certificate for Domain {domain} is set to expire "
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
        check_certs()
        # Generate a list of all available regions for EC2 and RDS
        regions_list = get_regions()
        # Check for compute running in the account
        check_ec2(regions_list)
        # Check for RDS databases running in the account
        check_rds(regions_list)
        if HOUSEKEEPING_ISSUES:
            logger.info(f"INFO! main HOUSEKEEPING_ISSUES: {HOUSEKEEPING_ISSUES}")
            post_to_slack(HOUSEKEEPING_ISSUES)
        else:
            post_to_slack(["No Housekeeping Needed"])
            logger.info(f"INFO! There are no certificates expiring soon, no compute found, and no databases found")
    except ClientError as ce:
        logger.error(f"ERROR! main ClientError {ce}")
