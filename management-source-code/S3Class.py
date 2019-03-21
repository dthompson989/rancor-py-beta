"""AWS S3 Bucket Management Class"""
from pathlib import Path
import mimetypes
from botocore.exceptions import ClientError


class S3Manager:
    """Manage S3 Buckets"""

    def __inti__(self, session):
        """Create bucket manager object"""
        self.session = session
        self.s3 = session.resource('s3')

    def all_buckets(self):
        """Return a list of all buckets"""
        return self.s3.buckets.all()

    def all_objects(self, bucket_name):
        """Return a list of the contents of a specified bucket"""
        return self.s3.Bucket(bucket_name).objects.all()

    def create_bucket(self, bucket_name):
        """Create an S3 bucket"""
        s3_bucket = None
        try:
            s3_bucket = self.s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': self.session.region_name}
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                s3_bucket = self.s3.Bucket(bucket_name)
            else:
                raise e

        return s3_bucket

    def set_policy(self, bucket):
        """Set a bucket policy to public"""
        policy = """{
                "Version":"2012-10-17",
                "Statement":[{
                    "Sid":"PublicReadGetObject",
                    "Effect":"Allow",
                    "Principal": "*",
                    "Action":["s3:GetObject"],
                    "Resource":["arn:aws:s3:::%s/*"]
                }]
            }""" % bucket.name

        policy = policy.strip()

        pol = bucket.Policy()
        pol.put(Policy=policy)

    def config_website(self, bucket):
        """Configure a pulic S3 bucket to be a website"""
        ws = bucket.Website()
        ws.put(WebsiteConfiguration={
            'ErrorDocument': {'Key': 'error.html'},
            'IndexDocument': {'Suffix': 'index.html'}
        })

    @staticmethod
    def push_website_content(bucket, path, key):
        """The method that actually pushes changes to S3"""
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'
        return bucket.upload_file(path, key, ExtraArgs={'ContentType': content_type})

    def code_sync(self, path, bucket_name):
        """Push code changes from local repo to AWS S3"""
        bucket = self.s3.Bucket(bucket_name)

        # pathlib is used to handle differences in unix/linux/windows file systems
        root = Path(path).expanduser().resolve()
        print('Syncing {} to AWS S3 Bucket {} . . . '.format(path, bucket))

        # Recursive function to traverse through a directory and
        def handle_directory(target):
            for p in target.iterdir():
                if p.is_dir():
                    handle_directory(p)
                if p.is_file():
                    self.push_website_content(bucket, str(p), str(p.relative_to(root)))

        handle_directory(root)
