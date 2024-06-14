# Standard Library
import os

# Third Party Library
import boto3

S3_QRCODE_LOG_BUCKET = os.environ["S3_QRCODE_LOG_BUCKET"]


class S3Client:

    def __init__(self, bucket_name: str = S3_QRCODE_LOG_BUCKET) -> None:
        self._bucket_name = bucket_name
        self.client = boto3.client("s3")

    def put_object(self, key: str, body: bytes) -> None:
        self.client.put_object(Bucket=self._bucket_name, Key=key, Body=body)
