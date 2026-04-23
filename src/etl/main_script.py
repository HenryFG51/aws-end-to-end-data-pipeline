"""
--------------------------------------------------------------------------------
@company      : 
@author       : Henry Fuentes
@created_data : 2026-03-10
@jira_task    : 
@description  :
                

-----------------------------------------------------------------------------------------------------------------------------------------------
"""

from extract_files import Get_Info


###########################PATHS################################
PATH_SALES = 'data-platform-lab/input/sales/sales.csv'
PATH_STORES = 'data-platform-lab/input/sales/stores.csv'
###########################PATHS################################



def main():
    print("Inicio del proceso de ETL")
    df_sales = Get_Info.extract_data_from_csv(PATH_SALES)
    df_stores = Get_Info.extract_data_from_csv(PATH_STORES)
    print(df_sales.head())
    print(df_sales.head())
    print("Fin del proceso de ETL")

if __name__ == "__main__":
    main()
    print("test1")