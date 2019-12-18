import boto3
from .config import BUCKET_NAME
from datetime import datetime


class AwsClient:
    def __init__(self):
        self.s3_client = boto3.client('s3')

    def upload_file_obj(self, file, bucket=BUCKET_NAME):
        """
        Function to upload a file_obj to an S3 bucket
        """
        key = f'{datetime.now().strftime("%d%m%y%H%M")}_{file.name}'
        self.s3_client.put_object(
            Body=file, Bucket=bucket, Key=key)

        # TODO update presigned urls?
        return key

    def generate_presigned_url(self, key, bucket=BUCKET_NAME):
        if key:
            return self.s3_client.generate_presigned_url('get_object',
                                                         Params={
                                                             'Bucket': bucket,
                                                             'Key': key,
                                                         },
                                                         ExpiresIn=36000)
        return None

    def download_file_obj(self, key, bucket=BUCKET_NAME):
        """
        Function to download a given file_obj from an S3 bucket
        """

        obj = self.s3_client.get_object(Bucket=bucket, Key=key)

        return obj

    def list_files(self, bucket=BUCKET_NAME):
        """
        Function to list files in a given S3 bucket
        """
        contents = []
        for item in self.s3_client.list_objects(Bucket=bucket)['Contents']:
            contents.append(item)

        return contents
