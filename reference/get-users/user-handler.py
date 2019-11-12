#!usr/bin/python
import botocore.vendored.requests as requests
import json
from botocore.vendored.requests.auth import HTTPBasicAuth
from botocore.vendored.requests.exceptions import HTTPError


def get_token(testing=None):
    """This function handles OAuth authentication to xMatters"""
    # Change to SSM dev/Xavier/xMattersApi
    token_url = "https://relx-np.hosted.xmatters.com/api/xm/1/oauth2/token"
    client_id = "9d3ec555-bb5c-402b-bb9e-53127eb4e01c"
    username = "NLN_SRE_API_User"
    password = "NLNSRE"
    # All ^ is in SSM now
    grant_type = "password"
    auth_dict = {'token': 'Bad Token', 'refresh_token': 'None'}

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
                auth_dict['refresh_token'] = rjson.get("refresh_token")
                print(f"INFO: OAuth Token Response {response}")
            else:
                print(f"ERROR: OAuth Token Failure {response}")
        except HTTPError as http_err:
            print(f"ERROR: HTTP Failure {http_err}")

    return auth_dict


def get_users():
    """This is the main xMatters pager function."""
    user_url = "https://relx-np.hosted.xmatters.com/api/xm/1/people?search=active"
    auth_token_dict = get_token("test")
    auth_token = auth_token_dict['token']

    try:
        response = requests.get(user_url, auth=auth_token)
        if response.status_code == 200:
            for user in response.json().get('data'):
                print(f"user_id: {user.get('id')} ::: Name: {user.get('firstName')} {user.get('lastName')}")
            print(f"Event triggered: {response.json()}")
            return response
        else:
            print(f"ERROR: Event Failure {str(response.status_code)}")
    except HTTPError as http_err:
        print(f"ERROR: Event Failure {http_err}")
    except TypeError as err:
        print(f"ERROR: Event Failure {err}")

    return False


def lambda_handler(event, context):
    user_data = get_users()
    if user_data:
        return {
            'statusCode': 200,
            'body': json.dumps("testPagerLambda Success!")
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps("testPagerLambda Failed!")
        }
