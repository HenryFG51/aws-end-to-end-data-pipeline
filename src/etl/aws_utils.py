# aws_utils.py
import json
import boto3
from typing import Optional
from botocore.exceptions import ClientError


class AWSOperations:
    def __init__(
        self,
        dynamo_table: str,
        secret_path: str,
        s3_bucket: Optional[str] = None,
        profile: Optional[str] = None,
        region: str = "us-east-1",
    ) -> None:
        """
        Constructor method of the aws operations.
        Creates the basic attributes to handle the communication
        with the aws services required by the ETL.

        Args:
            dynamo_table: (str) the DynamoDB table name with the ETL configurations.
            secret_path: (str) the secret path for Secrets Manager.
            s3_bucket: (str) the S3 bucket name to use. Default None.
            profile: (str) AWS CLI profile. Default None.
            region: (str) AWS region. Default us-east-1.

        Returns:
            None
        """
        self.dynamo_table = dynamo_table
        self.secret_path = secret_path
        self.s3_bucket = s3_bucket
        self.profile = profile
        self.region = region

        self.session = self._create_session()
        self.s3_client = self.session.client("s3")
        self.secrets_client = self.session.client("secretsmanager")
        self.dynamodb_resource = self.session.resource("dynamodb")
        self.dynamodb_client = self.session.client("dynamodb")

    def _create_session(self) -> boto3.Session:
        if self.profile:
            return boto3.Session(profile_name=self.profile, region_name=self.region)
        return boto3.Session(region_name=self.region)

    def get_secret(self) -> dict:
        try:
            response = self.secrets_client.get_secret_value(SecretId=self.secret_path)
            secret_string = response.get("SecretString", "{}")
            return json.loads(secret_string)
        except ClientError as e:
            raise RuntimeError(
                f"Error retrieving secret '{self.secret_path}': {e}"
            ) from e

    def get_dynamo_table(self):
        return self.dynamodb_resource.Table(self.dynamo_table)

    def upload_file_to_s3(self, file_path: str, key: str) -> None:
        if not self.s3_bucket:
            raise ValueError("s3_bucket is not configured.")

        try:
            self.s3_client.upload_file(file_path, self.s3_bucket, key)
            print(f"File uploaded to s3://{self.s3_bucket}/{key}")
        except ClientError as e:
            raise RuntimeError(
                f"Error uploading file to s3://{self.s3_bucket}/{key}: {e}"
            ) from e