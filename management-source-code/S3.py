"""AWS S3 Bucket Management Class"""
from pathlib import Path
import mimetypes
from botocore.exceptions import ClientError


class S3Manager:
    """Manage S3 Buckets"""

    def __inti__(self, session):
        """Create bucket manager object"""
        self.s3 = session.resource('s3')

    def all_buckets(self):
        """Return a list of all buckets"""
        return self.s3.buckets.all()

    def all_objects(self, bucket):
        """Return a list of the contents of a specified bucket"""
        return self.s3.Bucket(bucket).objects.all()

    def create_bucket(self, bucket):
        """Create an S3 bucket"""
        s3_bucket = None
        try:
            s3_bucket = self.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={'LocationConstraint': self.region_name}
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                s3_bucket = self.Bucket(bucket)
            else:
                raise e

        return s3_bucket
