"""
--------------------------------------------------------------------------------
@company      : 
@author       : Henry Fuentes
@created_data : 2026-03-10
@jira_task    : 
@description  :
                

-----------------------------------------------------------------------------------------------------------------------------------------------
"""

from transform_data import Get_Transform_Data
from extract_files import Get_Info

###########################PATHS################################
PATH_SALES = 'data-platform-lab/input/sales/sales.csv'
PATH_STORES = 'data-platform-lab/input/sales/stores.csv'
url = "https://dummyjson.com/products"
###########################PATHS################################

df_sales = Get_Info.extract_data_from_csv(PATH_SALES)
df_stores = Get_Info.extract_data_from_csv(PATH_STORES)
df_products = Get_Info.extract_data_from_api(url)


def main():
    print("Inicio del proceso de ETL")
    df_final = Get_Transform_Data.transform_data(df_sales, df_stores, df_products)
    print(df_final.head())
    print("Fin del proceso de ETL")

if __name__ == "__main__":
    main()
    print("test1")