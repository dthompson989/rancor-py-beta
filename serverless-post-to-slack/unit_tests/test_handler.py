#!usr/bin/python
"""A Python unit test for serverless-post-to-slack/handler.py"""
import boto3
import pytest
from botocore.exceptions import ClientError
from handler import post_to_slack
from moto import mock_s3


@mock_s3
def test_post_to_slack():
    """The lambda handler test function"""
    post_to_slack(open('unit_tests/s3_test.json', 'r').read(), "context")
    post_to_slack(open('unit_tests/sns_test.json', 'r').read(), "context")
