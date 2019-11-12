#!usr/bin/python
import boto3
import requests
import json
import logging
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_secret(session, region_name, secret_name):
    client = session.client(service_name='secretsmanager',
                            region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        logger.error(f"ERROR: {e}")
        return None
    else:
        if 'SecretString' in response:
            secret = json.loads(response['SecretString'])
            return secret


def get_recipients(base_url, token, group):
    """ This function returns the list of xMatters recipients to page"""
    users = []
    if group == "Demo":
        users.append({'id': 'thompsdm', 'recipientType': 'PERSON'})
    else:
        try:
            url = base_url + "/on-call?groups=" + group
            response = requests.post(url, auth="Bearer: " + token)
            #logger.info(f"INFO: get_recipients response {response}")
            print(f"INFO: get_recipients response {response}")
            if response.status_code == 200:
                response_json = response.json();
                for data in response_json['data']:
                    for member in data['members']['data']:
                        users.append({'id': member['member']['id'], 'recipientType': member['member']['recipientType']})
        except HTTPError as http_err:
            #logger.info(f"ERROR: Event Failure {http_err}")
            print(f"ERROR: Event Failure {http_err}")
    return users


def get_token(testing=None):
    """This function handles OAuth authentication to xMatters"""
    # Change to SSM dev/Xavier/xMattersApi
    token_url = "https://relx-np.hosted.xmatters.com/api/xm/1/oauth2/token"
    client_id = "9d3ec555-bb5c-402b-bb9e-53127eb4e01c"
    trigger_id = "782c648d-2e53-4f72-9ba7-1095a6318eb3"
    username = "NLN_SRE_API_User"
    password = "NLNSRE"
    # All ^ is in SSM now
    grant_type = "password"
    auth_dict = {'token': 'Bad Token',
                 'refresh_token': 'None',
                 'headers': {'Content-Type': 'application/json'},
                 'trigger_id': trigger_id}

    if testing:
        auth_dict['token'] = HTTPBasicAuth(username, password)
    else:
        payload = {
            'grant_type': grant_type,
            'client_id': client_id,
            'username': username,
            'password': password,
        }
        try:
            response = requests.post(token_url, json=payload)

            if response.status_code == 200:
                rjson = response.json()
                auth_dict['token'] = rjson.get('access_token')
                auth_dict['headers'] = {'Content-Type': 'application/json',
                                        'Authorization': 'Bearer ' + rjson.get('access_token')}
                auth_dict['refresh_token'] = rjson.get("refresh_token")
                #logger.info(f"INFO: OAuth Token Response {response}")
                print(f"INFO: OAuth Token Response {response}")
            else:
                #logger.info(f"ERROR: OAuth Token Failure {response}")
                print(f"ERROR: OAuth Token Failure {response}")
        except HTTPError as http_err:
            print(f"ERROR: HTTP Failure {http_err}")

    return auth_dict


def pager(request):
    """This is the main xMatters pager function."""
    pager_base_url = "https://relx-np.hosted.xmatters.com/api/integration/1"
    auth_token_dict = get_token("test")
    auth_token = auth_token_dict['token']
    headers = auth_token_dict['headers']
    trigger_url = pager_base_url + "/functions/" + auth_token_dict['trigger_id'] + "/triggers"
    recipients = get_recipients(pager_base_url, auth_token, "Demo")
    if recipients:
        incident = "INC00000001"
        comment = "Demo Comment"
        data = {
            'properties': {
                'number': incident,
                'comment': comment
            },
            'recipients': recipients
        }
        data_string = json.dumps(data)
        try:
            response = requests.post(trigger_url, headers=headers, data=data_string, auth=auth_token)
            if response.status_code == 202:
                #logger.info(f"Event triggered: {response.json()['requestId']}")
                print(f"Event triggered: {response.json()['requestId']}")
                return True
            else:
                #logger.info(f"ERROR: Event Failure {str(response.status_code)}")
                print(f"ERROR: Event Failure {str(response.status_code)}")
        except HTTPError as http_err:
            #logger.info(f"ERROR: Event Failure {http_err}")
            print(f"ERROR: Event Failure {http_err}")
        except TypeError as err:
            # logger.info(f"ERROR: Event Failure {http_err}")
            print(f"ERROR: Event Failure {err}")
    else:
        #logger.info(f"ERROR: {request}")
        print(f"ERROR: {request}")
    return False


def lambda_handler(event, context):
    paged = pager("TEST PAGE")
    if paged:
        return {
            'statusCode': 200,
            'body': json.dumps("Hello from testPagerLambda!")
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps("testPagerLambda Failed!")
        }
