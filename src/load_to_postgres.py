"""
Step 3 — Load the Step 2 CSVs into PostgreSQL.
Run schema.sql first to create the tables, then run this script.

Usage:
    python src/load_to_postgres.py
"""
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()  # reads DB_* values from a .env file in the project root

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "urban_threads")

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Order matters: parents before children, to satisfy foreign keys
TABLES_IN_ORDER = [
    "stores",
    "products",
    "customers",
    "orders",
    "order_items",
    "inventory",
    "returns",
    "discounts",
]

for table in TABLES_IN_ORDER:
    csv_path = f"data/raw/{table}.csv"
    df = pd.read_csv(csv_path)
    df.to_sql(table, engine, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into {table}")

print("All tables loaded.")
