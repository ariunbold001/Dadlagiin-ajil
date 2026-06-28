import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection
engine = create_engine(
    "postgresql://Ariunbold:9119@localhost:5432/Dadlaga_ajil"
)

print("Loading customers...")
customers = pd.read_csv("customers.csv")

customers.to_sql(
    "customers",
    engine,
    if_exists="append",
    index=False,
    method="multi"
)

print("Loading accounts...")
accounts = pd.read_csv("accounts.csv")

accounts.to_sql(
    "accounts",
    engine,
    if_exists="append",
    index=False,
    method="multi"
)

print("Loading loans...")
loans = pd.read_csv("loans.csv")

loans.to_sql(
    "loans",
    engine,
    if_exists="append",
    index=False,
    method="multi"
)

print("Loading transactions...")

for chunk in pd.read_csv(
        "transactions.csv",
        chunksize=50000):

    chunk.to_sql(
        "transactions",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print(f"{len(chunk)} rows inserted")

print("ETL Completed Successfully!")