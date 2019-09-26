#!usr/bin/python
"""A Python unit test for serverless-post-to-slack/handler.py"""
import boto3
import pytest
from botocore.exceptions import ClientError
import importlib.util
from moto import mock_s3

"""Import the post to slack module"""
spec = importlib.util.spec_from_file_location('post_to_slack', '../handler.py')
slack_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(slack_module)


@mock_s3
def test_post_to_slack():
    """The lambda handler test function"""
    slack_module.post_to_slack(open('unit_tests/s3_test.json', 'r').read(), "context")
    slack_module.post_to_slack(open('unit_tests/sns_test.json', 'r').read(), "context")
