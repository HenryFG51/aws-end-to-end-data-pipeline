from extract_files import Get_Info
import pandas as pd

class Get_Transform_Data:
    
    @staticmethod
    def transform(df_sales, df_stores, df_products):
        # Create copies of input dataframes to avoid modifying originals
        # Crear copias de los dataframes de entrada para evitar modificar los originales
        df_sales = df_sales.copy()
        df_stores = df_stores.copy()
        df_products = df_products.copy()

        # Normalize column names to lowercase and strip whitespace
        # Normalizar nombres de columnas a minúsculas y eliminar espacios en blanco
        df_sales.columns = [c.lower().strip() for c in df_sales.columns]
        df_stores.columns = [c.lower().strip() for c in df_stores.columns]
        df_products.columns = [c.lower().strip() for c in df_products.columns]

        # Convert quantity and unit_price columns to numeric types, coercing errors to NaN
        # Convertir columnas quantity y unit_price a tipos numéricos, forzando errores a NaN
        df_sales["quantity"] = pd.to_numeric(df_sales["quantity"], errors="coerce")
        df_sales["unit_price"] = pd.to_numeric(df_sales["unit_price"], errors="coerce")

        # Clean data: remove rows with missing product_id or store_id, and drop duplicates
        # Limpiar datos: eliminar filas con product_id o store_id faltantes, y eliminar duplicados
        df_sales = df_sales.dropna(subset=["product_id", "store_id"])
        df_sales = df_sales.drop_duplicates()

        # Calculate revenue as quantity multiplied by unit_price
        # Calcular ingresos como cantidad multiplicada por precio unitario
        df_sales["revenue"] = df_sales["quantity"] * df_sales["unit_price"]

        # Adjust products dataframe: rename columns and select relevant columns
        # Ajustar dataframe de productos: renombrar columnas y seleccionar columnas relevantes
        df_products = df_products.rename(columns={
            "id": "product_id",
            "title": "product_name"
        })

        df_products = df_products[["product_id", "product_name", "category", "brand"]]

        # Merge sales data with products data on product_id (left join)
        # Fusionar datos de ventas con datos de productos en product_id (unión izquierda)
        df_final = df_sales.merge(df_products, on="product_id", how="left")

        # Merge the result with stores data on store_id (left join)
        # Fusionar el resultado con datos de tiendas en store_id (unión izquierda)
        df_final = df_final.merge(df_stores, on="store_id", how="left")

        print(f"[TRANSFORM] Final dataset rows: {len(df_final)}")

        return df_final