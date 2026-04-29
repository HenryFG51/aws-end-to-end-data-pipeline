"""
--------------------------------------------------------------------------------
@company      : 
@author       : Henry Fuentes
@created_data : 2026-03-10
@jira_task    : 
@description  :
                

-----------------------------------------------------------------------------------------------------------------------------------------------
"""

# Import necessary modules for data transformation and extraction
# Importar módulos necesarios para transformación y extracción de datos
from transform_data import Get_Transform_Data
from extract_files import Get_Info
import awswrangler as wr
import boto3
from awsglue.utils import getResolvedOptions
from aws_utils import AWSOperations
import sys
from datetime import datetime


#get datatime
execution_date = datetime.today()
year = execution_date.strftime("%Y")
month = execution_date.strftime("%m")
day = execution_date.strftime("%d")


# Get resolved options from command line arguments for AWS Glue job
# Obtener opciones resueltas de argumentos de línea de comandos para el trabajo de AWS Glue
args = getResolvedOptions(sys.argv,['output_s3', 'dynamodb_table_name'])

# Initialize AWS operations object with DynamoDB table, secret path, S3 bucket, and region
# Inicializar objeto de operaciones AWS con tabla DynamoDB, ruta secreta, bucket S3 y región
aws_ops = AWSOperations(
    dynamo_table=args['dynamodb_table_name'],
    secret_path=None,
    s3_bucket=args['output_s3'],
    profile=None,
    region="us-east-1"
)

# Retrieve secrets from AWS Secrets Manager
# Recuperar secretos de AWS Secrets Manager
#secrets = aws_ops.get_secret()
s3_bucket = f"{args['output_s3']}"

# Define file paths and API URL for data sources
# Definir rutas de archivos y URL de API para fuentes de datos
###########################PATHS################################
PATH_SALES = 'data-platform-lab/input/sales/sales.csv'
PATH_STORES = 'data-platform-lab/input/stores/stores.csv'
PATH_RAW = 'data-platform-lab/raw'
PATH_PROCESSED = 'data-platform-lab/processed/sales_enriched/'
url = "https://dummyjson.com/products"
###########################PATHS################################

# Define the Load_Data class for handling data loading operations
# Definir la clase Load_Data para manejar operaciones de carga de datos
class Get_Load_Data:
    
    @staticmethod
    def load_data():
        # Placeholder for loading the final DataFrame to database or storage
        # Aquí iría la lógica para cargar el DataFrame final a la base de datos o almacenamiento deseado
        print("Leer los datos de las fuentes")

        # Extract sales data from CSV file
        # Extraer datos de ventas desde archivo CSV
        df_sales = Get_Info.extract_data_from_csv(PATH_SALES)
        s3_destination_path = f's3://{s3_bucket}/{PATH_RAW}'
        wr.s3.to_csv(df=df_sales, path=f'{s3_destination_path}/{year}/{month}/{day}/sales.csv',index=False)
        # Extract stores data from CSV file
        # Extraer datos de tiendas desde archivo CSV
        df_stores = Get_Info.extract_data_from_csv(PATH_STORES)
        s3_destination_path = f's3://{s3_bucket}/{PATH_RAW}'
        wr.s3.to_csv(df=df_stores,path=f'{s3_destination_path}/{year}/{month}/{day}/stores.csv',index=False)
        # Extract products data from API
        # Extraer datos de productos desde API
        df_products = Get_Info.extract_data_from_api(url)
        s3_destination_path = f's3://{s3_bucket}/{PATH_RAW}'
        wr.s3.to_csv(df=df_products,path=f'{s3_destination_path}/{year}/{month}/{day}/products.csv',index=False)

        print("Los datos han sido leídos correctamente")

        print("Transformar los datos")
        # Transform the extracted data using the transform method
        # Transformar los datos extraídos usando el método de transformación
        df_final = Get_Transform_Data.transform(df_sales, df_stores, df_products)
        print("Los datos han sido transformados correctamente")

        # Commented out: Save DataFrame to Parquet file in S3
        # Comentado: Guardar DataFrame en archivo Parquet en S3
        s3_destination_path = f's3://{s3_bucket}/{PATH_PROCESSED}'
        wr.s3.to_parquet(df=df_final,path=s3_destination_path,database='data_platform_dev_db',table='sales_enriched',mode="overwrite",dataset=True)
        pass