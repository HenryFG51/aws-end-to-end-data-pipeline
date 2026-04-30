"""
--------------------------------------------------------------------------------
@company      : 
@author       : Henry Fuentes
@created_data : 2026-03-10
@jira_task    : 
@description  :
                

-----------------------------------------------------------------------------------------------------------------------------------------------
"""
from Load_Data import Get_Load_Data

def main():
    # Print start of ETL process
    # Imprimir inicio del proceso ETL
    print("Inicio del proceso de ETL")
    Get_Load_Data.load_data()
    print("Fin del proceso de ETL")

# Execute main function if script is run directly
# Ejecutar función principal si el script se ejecuta directamente
if __name__ == "__main__":
    main()