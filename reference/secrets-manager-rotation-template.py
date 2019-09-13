# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import boto3
import logging
import json
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """Secrets Manager Rotation Template
    This is a template for creating an AWS Secrets Manager rotation lambda
    Args:
        event (dict): Lambda dictionary of event parameters. These keys must include the following:
            - SecretId: The secret ARN or identifier
            - ClientRequestToken: The ClientRequestToken of the secret version
            - Step: The rotation step (one of createSecret, setSecret, testSecret, or finishSecret)
        context (LambdaContext): The Lambda runtime information
    Raises:
        ResourceNotFoundException: If the secret with the specified arn and stage does not exist
        ValueError: If the secret is not properly configured for rotation
        KeyError: If the event parameters do not contain the expected keys
    """
    arn = event['SecretId']
    token = event['ClientRequestToken']
    step = event['Step']

    # Setup the client
    service_client = boto3.client('secretsmanager', endpoint_url=os.environ['SECRETS_MANAGER_ENDPOINT'])

    # Make sure the version is staged correctly
    metadata = service_client.describe_secret(SecretId=arn)
    if not metadata['RotationEnabled']:
        logger.error("Secret %s is not enabled for rotation" % arn)
        raise ValueError("Secret %s is not enabled for rotation" % arn)
    versions = metadata['VersionIdsToStages']
    if token not in versions:
        logger.error("Secret version %s has no stage for rotation of secret %s." % (token, arn))
        raise ValueError("Secret version %s has no stage for rotation of secret %s." % (token, arn))
    if "AWSCURRENT" in versions[token]:
        logger.info("Secret version %s already set as AWSCURRENT for secret %s." % (token, arn))
        return
    elif "AWSPENDING" not in versions[token]:
        logger.error("Secret version %s not set as AWSPENDING for rotation of secret %s." % (token, arn))
        raise ValueError("Secret version %s not set as AWSPENDING for rotation of secret %s." % (token, arn))

    if step == "createSecret":
        create_secret(service_client, arn, token)

    elif step == "setSecret":
        set_secret(service_client, arn, token)

    elif step == "testSecret":
        test_secret(service_client, arn, token)

    elif step == "finishSecret":
        finish_secret(service_client, arn, token)

    else:
        raise ValueError("Invalid step parameter")


def create_secret(service_client, arn, token):
    """Create the secret
    This method first checks for the existence of a secret for the passed in token. If one does not exist, it will
    generate a new secret and put it with the passed in token.
    Args:
        service_client (client): The secrets manager service client
        arn (string): The secret ARN or other identifier
        token (string): The ClientRequestToken associated with the secret version
    Raises:
        ResourceNotFoundException: If the secret with the specified arn and stage does not exist
    """
    # Make sure the current secret exists
    service_client.get_secret_value(SecretId=arn, VersionStage="AWSCURRENT")

    # Now try to get the secret version, if that fails, put a new secret
    try:
        service_client.get_secret_value(SecretId=arn, VersionId=token, VersionStage="AWSPENDING")
        logger.info("createSecret: Successfully retrieved secret for %s." % arn)
    except service_client.exceptions.ResourceNotFoundException:
        # Generate a random password
        passwd = service_client.get_random_password(ExcludeCharacters='/@"\'\\')

        # Put the secret
        service_client.put_secret_value(SecretId=arn, ClientRequestToken=token, SecretString=passwd['RandomPassword'],
                                        VersionStages=['AWSPENDING'])
        logger.info("createSecret: Successfully put secret for ARN %s and version %s." % (arn, token))


def set_secret(service_client, arn, token):
    """Set the secret
    This method should set the AWSPENDING secret in the service that the secret belongs to. For example, if the secret
    is a database credential, this method should take the value of the AWSPENDING secret and set the user's password to
    this value in the database.
    Args:
        service_client (client): The secrets manager service client
        arn (string): The secret ARN or other identifier
        token (string): The ClientRequestToken associated with the secret version
    """
    # This is where the secret should be set in the service
    """ This is the xquery that would update/change a ML user.
    Execute this against the security database
        xquery version "1.0-ml";
        import module namespace sec="http://marklogic.com/xdmp/security" at "/MarkLogic/security.xqy";
        sec:user-set-password("Jim", "temp")
    
    Changes the password for the user, "Jim," to "temp."
    This line would clear the local cache for that user. Would need to be run on E Nodes, maybe D Nodes too.
    
        sec:external-security-clear-cache("Jim")

    Clears the login cache in the external authorization configuration object, named "Jim".
    
    There is an example python script to connect to ML CSR-XQuery/XQuery/testCSRMLCalls.py
    """
    raise NotImplementedError


def test_secret(service_client, arn, token):
    """Test the secret
    This method should validate that the AWSPENDING secret works in the service that the secret belongs to. For example,
    if the secret is a database credential, this method should validate that the user can login with the password in
    AWSPENDING and that the user has all of the expected permissions against the database.
    Args:
        service_client (client): The secrets manager service client
        arn (string): The secret ARN or other identifier
        token (string): The ClientRequestToken associated with the secret version
    """
    # This is where the secret should be tested against the service
    raise NotImplementedError


def finish_secret(service_client, arn, token):
    """Finish the secret
    This method finalizes the rotation process by marking the secret version passed in as the AWSCURRENT secret.
    Args:
        service_client (client): The secrets manager service client
        arn (string): The secret ARN or other identifier
        token (string): The ClientRequestToken associated with the secret version
    Raises:
        ResourceNotFoundException: If the secret with the specified arn does not exist
    """
    # First describe the secret to get the current version
    metadata = service_client.describe_secret(SecretId=arn)
    current_version = None
    for version in metadata["VersionIdsToStages"]:
        if "AWSCURRENT" in metadata["VersionIdsToStages"][version]:
            if version == token:
                # The correct version is already marked as current, return
                logger.info("finishSecret: Version %s already marked as AWSCURRENT for %s" % (version, arn))
                return
            current_version = version
            break

    # Finalize by staging the secret version current
    service_client.update_secret_version_stage(SecretId=arn, VersionStage="AWSCURRENT", MoveToVersionId=token,
                                               RemoveFromVersionId=current_version)
    logger.info("finishSecret: Successfully set AWSCURRENT stage to version %s for secret %s." % (token, arn))


# This is written for SQL server, so translate to what ML would need.
def get_connection(secret_dict):
    """Gets a connection to SQL Server DB from a secret dictionary
    This helper function tries to connect to the database grabbing connection info
    from the secret dictionary. If successful, it returns the connection, else None
    Args:
        secret_dict (dict): The Secret Dictionary
    Returns:
        Connection: The pymssql.Connection object if successful. None otherwise
    Raises:
        KeyError: If the secret json does not contain the expected keys
    """
    # Parse and validate the secret JSON string
    port = str(secret_dict['port']) if 'port' in secret_dict else '1433'
    dbname = secret_dict['dbname'] if 'dbname' in secret_dict else 'master'

    # Try to obtain a connection to the db
    try:
        conn = pymssql.connect(server=secret_dict['host'],
                               user=secret_dict['username'],
                               password=secret_dict['password'],
                               database=dbname,
                               port=port,
                               login_timeout=5,
                               as_dict=True)
        return conn
    except pymssql.OperationalError:
        return None