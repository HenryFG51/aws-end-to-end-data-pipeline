"""
--------------------------------------------------------------------------------
@company      : 
@author       : Henry Fuentes
@created_data : 2026-03-10
@jira_task    : 
@description  :
                

-----------------------------------------------------------------------------------------------------------------------------------------------
"""
import sys
import requests
import pandas as pd
import boto3
from awsglue.utils import getResolvedOptions
from aws_utils import AWSOperations
import awswrangler as wr


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

url = base_url

response = requests.get(url)
response.raise_for_status()

data = response.json()
df = pd.DataFrame(data["response"])
columns = ['title', 'competition', 'date']

df_final = df[columns]

#saving data frame in a parquet file
s3_destination_path = f's3://{s3_bucket}/data-platform-lab/Soccer_Files/'
wr.s3.to_parquet(df=df_final,path=s3_destination_path,database='data_platform_dev_db',table='soccer_data',mode="overwrite_partitions",dataset=True)

#function to store the dataframe in a table 
# def write_to_s3(df, s3_bucket, path_iati, sub_path, table_name, dtype=None):
#     s3_destination_path = f's3://{s3_bucket}/{path_iati}/{sub_path}/'
#     wr.s3.to_parquet(
#         df=df,
#         path=s3_destination_path,
#         database='iadb-dmt-db',
#         table=table_name,
#         mode="overwrite",
#         dataset=True,
#         dtype=dtype
#         )

# write_to_s3(df_final, s3_test_row, path_test, 'locations_projects_AFP', 'edw_dmt_iati_locations_projects_AFP')