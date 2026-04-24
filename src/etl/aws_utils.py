# aws_utils.py
# Import necessary libraries for JSON handling, AWS SDK, typing, and error handling
# Importar bibliotecas necesarias para manejo de JSON, SDK de AWS, tipado y manejo de errores
import json
import boto3
from typing import Optional
from botocore.exceptions import ClientError

# Define the AWSOperations class for handling AWS service interactions
# Definir la clase AWSOperations para manejar interacciones con servicios AWS
class AWSOperations:
    # Initialize the AWSOperations class with required parameters
    # Inicializar la clase AWSOperations con parámetros requeridos
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
        # Set instance attributes for DynamoDB table, secret path, S3 bucket, profile, and region
        # Establecer atributos de instancia para tabla DynamoDB, ruta secreta, bucket S3, perfil y región
        self.dynamo_table = dynamo_table
        self.secret_path = secret_path
        self.s3_bucket = s3_bucket
        self.profile = profile
        self.region = region

        # Create AWS session and initialize clients/resources
        # Crear sesión AWS e inicializar clientes/recursos
        self.session = self._create_session()
        self.s3_client = self.session.client("s3")
        self.secrets_client = self.session.client("secretsmanager")
        self.dynamodb_resource = self.session.resource("dynamodb")
        self.dynamodb_client = self.session.client("dynamodb")

    # Private method to create AWS session based on profile or region
    # Método privado para crear sesión AWS basado en perfil o región
    def _create_session(self) -> boto3.Session:
        if self.profile:
            return boto3.Session(profile_name=self.profile, region_name=self.region)
        return boto3.Session(region_name=self.region)

    # Retrieve secret from AWS Secrets Manager
    # Recuperar secreto de AWS Secrets Manager
    def get_secret(self) -> dict:
        try:
            response = self.secrets_client.get_secret_value(SecretId=self.secret_path)
            secret_string = response.get("SecretString", "{}")
            return json.loads(secret_string)
        except ClientError as e:
            raise RuntimeError(
                f"Error retrieving secret '{self.secret_path}': {e}"
            ) from e

    # Get DynamoDB table resource
    # Obtener recurso de tabla DynamoDB
    def get_dynamo_table(self):
        return self.dynamodb_resource.Table(self.dynamo_table)

    # Upload file to S3 bucket
    # Subir archivo al bucket S3
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