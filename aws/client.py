import boto3
from .config import BUCKET_NAME
from datetime import datetime


class AwsClient:
    def upload_file_obj(self, file, bucket=BUCKET_NAME):
        """
        Function to upload a file_obj to an S3 bucket
        """
        key = f'{datetime.now().strftime("%d%m%y%H%M")}_{file.name}'
        s3_client = boto3.client('s3')
        s3_client.put_object(
            Body=file, Bucket=bucket, Key=key)
        url = s3_client.generate_presigned_url('get_object',
                                               Params={
                                                   'Bucket': bucket,
                                                   'Key': key,
                                               },
                                               ExpiresIn=36000)
        #TODO update presigned urls?
        return url

    def download_file_obj(self, key, bucket=BUCKET_NAME):
        """
        Function to download a given file_obj from an S3 bucket
        """

        s3_client = boto3.client('s3')
        obj = s3_client.get_object(Bucket=bucket, Key=key)

        return obj

    def list_files(self, bucket=BUCKET_NAME):
        """
        Function to list files in a given S3 bucket
        """
        s3 = boto3.client('s3')
        contents = []
        for item in s3.list_objects(Bucket=bucket)['Contents']:
            contents.append(item)

        return contents
