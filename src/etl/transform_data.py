from extract_files import Get_Info
import pandas as pd

class Get_Transform_Data:

    @staticmethod
    def transform_data(df_sales, df_stores, df_products):

        df_sales = df_sales.copy()
        df_stores = df_stores.copy()
        df_products = df_products.copy()

        # Normalizar columnas
        df_sales.columns = [c.lower().strip() for c in df_sales.columns]
        df_stores.columns = [c.lower().strip() for c in df_stores.columns]
        df_products.columns = [c.lower().strip() for c in df_products.columns]

        # Tipos
        df_sales["quantity"] = pd.to_numeric(df_sales["quantity"], errors="coerce")
        df_sales["unit_price"] = pd.to_numeric(df_sales["unit_price"], errors="coerce")

        # Limpieza
        df_sales = df_sales.dropna(subset=["product_id", "store_id"])
        df_sales = df_sales.drop_duplicates()

        # Revenue
        df_sales["revenue"] = df_sales["quantity"] * df_sales["unit_price"]

        # Ajustar productos API
        df_products = df_products.rename(columns={
            "id": "product_id",
            "title": "product_name"
        })

        df_products = df_products[["product_id", "product_name", "category", "brand"]]

        # Join productos
        df_final = df_sales.merge(df_products, on="product_id", how="left")

        # Join tiendas
        df_final = df_final.merge(df_stores, on="store_id", how="left")

        print(f"[TRANSFORM] Final dataset rows: {len(df_final)}")

        return df_final