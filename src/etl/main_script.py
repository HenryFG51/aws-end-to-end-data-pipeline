"""
--------------------------------------------------------------------------------
@company      : 
@author       : Henry Fuentes
@created_data : 2026-03-10
@jira_task    : 
@description  :
                

-----------------------------------------------------------------------------------------------------------------------------------------------
"""

from extract_files import extract_data_from_csv

def main():
    print("Inicio del proceso de ETL")
    df = extract_data_from_csv()
    print(df.head())
    print("Fin del proceso de ETL")

if __name__ == "__main__":
    main()