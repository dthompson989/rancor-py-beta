"""AWS S3 Bucket Management Class"""
from pathlib import Path
import mimetypes
import boto3
from botocore.exceptions import ClientError
import util
from hashlib import md5
import hashlib
from functools import reduce


class S3Manager:
    """Manage S3 Buckets"""

    CHUNK_SIZE = 8388608

    def __init__(self, session):
        """Create bucket manager object"""
        self.session = session
        self.s3 = self.session.resource('s3')
        self.transfer_config = boto3.s3.transfer.TransferConfig(
            multipart_chunksize=self.CHUNK_SIZE,
            multipart_threshold=self.CHUNK_SIZE
        )
        self.manifest = {}
        self.upload_count = 0

    def get_region_name(self, bucket):
        """Get the bucket's region name"""
        client = self.s3.meta.client
        bucket_az = client.get_bucket_location(Bucket=bucket.name)

        return bucket_az["LocationConstraint"] or 'us-east-1'

    def get_bucket_url(self, bucket):
        """Get the S3 website URL for this bucket"""
        return "http://{}.{}".format(bucket.name, util.get_endpoint(self.get_region_name(bucket)).host)

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

        print('Bucket Created: ' + bucket_name)
        return s3_bucket

    @staticmethod
    def set_policy(bucket):
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

    @staticmethod
    def config_website(bucket):
        """Configure a pulic S3 bucket to be a website"""
        ws = bucket.Website()
        ws.put(WebsiteConfiguration={
            'ErrorDocument': {'Key': 'error.html'},
            'IndexDocument': {'Suffix': 'index.html'}
        })

    def load_manifest(self, bucket):
        """Load manifest for caching"""
        paginator = self.s3.meta.client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket.name):
            for obj in page.get('Contents', []):
                self.manifest[obj['Key']] = obj['ETag']

    @staticmethod
    def hash_data(data):
        """Generic hash function"""
        data_hash = md5()
        data_hash.update(data)

        return data_hash

    def gen_etag(self, path):
        """Generate the ETag to see if a file has changed recently, so only files that have changed are synced to S3"""
        hashes = []

        with open(path, 'rb') as f:
            while True:
                data = f.read(self.CHUNK_SIZE)
                if not data:
                    break
                hashes.append(self.hash_data(data))

        if not hashes:
            return
        elif len(hashes) == 1:
            return '"{}"'.format(hashes[0].hexdigest())
        else:
            chunk_hash = self.hash_data(reduce(lambda x, y: x + y, (h.digest() for h in hashes)))
            return '"{}-{}"'.format(chunk_hash.hexdigest(), len(hashes))

    def push_website_content(self, bucket, path, key):
        """The method that actually pushes changes to S3"""
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'

        etag = self.gen_etag(path)
        if self.manifest.get(key, '') == etag:
            return

        print("Syncing {}".format(path))
        self.upload_count += 1
        return bucket.upload_file(
            path,
            key,
            ExtraArgs={'ContentType': content_type},
            Config=self.transfer_config
        )

    def code_sync(self, path, bucket_name):
        """Push code changes from local repo to AWS S3"""
        bucket = self.s3.Bucket(bucket_name)
        self.load_manifest(bucket)

        # pathlib is used to handle differences in unix/linux/windows file systems
        root = Path(path).expanduser().resolve()

        print('Syncing {} to AWS S3 Bucket {} . . . '.format(path, bucket_name))
        print('-------------------------------------------------------------------------------')

        # Recursive function to traverse through a directory and
        def handle_directory(target):
            for p in target.iterdir():
                if p.is_dir():
                    handle_directory(p)
                if p.is_file():
                    self.push_website_content(bucket, str(p), str(p.relative_to(root)))

        handle_directory(root)
        print('-------------------------------------------------------------------------------')
        print('Code Sync Complete!')
        print('Synced {} Documents'.format(self.upload_count))
        print('S3 Endpoint URL: ' + self.get_bucket_url(bucket))

