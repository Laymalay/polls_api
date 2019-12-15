import boto3
from .config import BUCKET_NAME


class AwsClient:
    def upload_file(self, file_name, bucket=BUCKET_NAME):
        """
        Function to upload a file to an S3 bucket
        """
        object_name = file_name
        s3_client = boto3.client('s3')
        response = s3_client.upload_file(file_name, bucket, object_name)

        return response

    def download_file(self, file_name, bucket=BUCKET_NAME):
        """
        Function to download a given file from an S3 bucket
        """
        s3 = boto3.resource('s3')
        output = f"downloads/{file_name}"
        s3.Bucket(bucket).download_file(file_name, output)

        return output

    def list_files(self, bucket=BUCKET_NAME):
        """
        Function to list files in a given S3 bucket
        """
        s3 = boto3.client('s3')
        contents = []
        for item in s3.list_objects(Bucket=bucket)['Contents']:
            contents.append(item)

        return contents
