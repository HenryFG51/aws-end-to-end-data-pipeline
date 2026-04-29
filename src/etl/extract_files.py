"""
--------------------------------------------------------------------------------
@company      : 
@author       : Henry Fuentes
@created_data : 2026-04-22
@jira_task    : 
@description  : por medio de este script vamos a hacer la extraccion de los datos de los archivos .csv y luego se van a cargar a la base de datos 
                

-----------------------------------------------------------------------------------------------------------------------------------------------
"""

# Import necessary libraries for system operations, HTTP requests, data manipulation, and AWS services
# Importar bibliotecas necesarias para operaciones del sistema, solicitudes HTTP, manipulación de datos y servicios AWS
import sys
import requests
import pandas as pd
import boto3
from awsglue.utils import getResolvedOptions
from aws_utils import AWSOperations
import awswrangler as wr

# Get resolved options from command line arguments for AWS Glue job
# Obtener opciones resueltas de argumentos de línea de comandos para el trabajo de AWS Glue
args = getResolvedOptions(sys.argv,['output_s3', 'dynamodb_table_name'])

# Initialize AWS operations object with DynamoDB table, secret path, S3 bucket, and region
# Inicializar objeto de operaciones AWS con tabla DynamoDB, ruta secreta, bucket S3 y región
aws_ops = AWSOperations(
    dynamo_table=args['dynamodb_table_name'],
    s3_bucket=args['output_s3'],
    profile=None,
    region="us-east-1"
)

# Retrieve secrets from AWS Secrets Manager
# Recuperar secretos de AWS Secrets Manager
secrets = aws_ops.get_secret()
s3_bucket = f"{args['output_s3']}"

# Define the Get_Info class for data extraction operations
# Definir la clase Get_Info para operaciones de extracción de datos
class Get_Info:

    @staticmethod
    def extract_data_from_csv(path):
        # Read CSV data from S3 bucket using AWS Wrangler
        # Leer datos CSV desde bucket S3 usando AWS Wrangler
        df = wr.s3.read_csv(f's3://{s3_bucket}/{path}',encoding='latin-1')
        return df
    
    @staticmethod
    def extract_data_from_api(endpoint):
        # Make HTTP GET request to the API endpoint
        # Hacer solicitud HTTP GET al endpoint de la API
        response = requests.get(endpoint, timeout=30)
        if response.status_code == 200:
            # Parse JSON response and create DataFrame from products data
            # Analizar respuesta JSON y crear DataFrame desde datos de productos
            data = response.json()
            df = pd.DataFrame(data['products'])
            return df
        else:
            # Print error message if API request fails
            # Imprimir mensaje de error si la solicitud a la API falla
            print(f"Error al obtener datos de la API: {response.status_code}")
            return None
    