#!usr/bin/python
"""A Python unit test for perverless-post-to-slack/handler.py"""
import boto3
import pytest
from botocore.exceptions import ClientError
from handler import post_to_slack
from moto import mock_s3


@mock_s3
def test_post_to_slack():
    """The lambda handler test function"""
