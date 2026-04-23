"""
--------------------------------------------------------------------------------
@company      : 
@author       : Henry Fuentes
@created_data : 2026-04-22
@jira_task    : 
@description  : por medio de este script vamos a hacer la extraccion de los datos de los archivos .csv y luego se van a cargar a la base de datos 
                

-----------------------------------------------------------------------------------------------------------------------------------------------
"""

import sys
import requests
import pandas as pd
import boto3
from awsglue.utils import getResolvedOptions
from aws_utils import AWSOperations
import awswrangler as wr


###########################PATHS################################
PATH_SALES = 'data-platform-lab/input/sales/sales.csv'
###########################PATHS################################


args = getResolvedOptions(sys.argv,['secret_manager', 'output_s3', 'dynamodb_table_name'])

aws_ops = AWSOperations(
    dynamo_table=args['dynamodb_table_name'],
    secret_path=args['secret_manager'],
    s3_bucket=args['output_s3'],
    profile=None,
    region="us-east-1"
)

secrets = aws_ops.get_secret()
base_url = secrets["sports_api_base_url"]
s3_bucket = f"{args['output_s3']}"

print(base_url)
print(s3_bucket)

def extract_data_from_csv():
    df = wr.s3.read_csv(f's3://{s3_bucket}/{PATH_SALES}',encoding='latin-1')
    #df = wr.s3.read_csv('s3://data-platform-dev-main-570435244160/data-platform-lab/input/sales/sales.csv',encoding='latin-1')
    return df

#s3://data-platform-dev-main-570435244160/data-platform-lab/input/sales/sales.csv


#saving data frame in a parquet file
# s3_destination_path = f's3://{s3_bucket}/data-platform-lab/Soccer_Files/'
# wr.s3.to_parquet(df=df_final,path=s3_destination_path,database='data_platform_dev_db',table='soccer_data',mode="overwrite_partitions",dataset=True)