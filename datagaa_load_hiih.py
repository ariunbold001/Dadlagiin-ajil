import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://Ariunbold:9119@localhost:5432/Dadlaga_ajil"
)

print("Loading customers...")
customers = pd.read_csv("uilchluulegch.csv")
customers.to_sql("customers", engine, if_exists="append", index=False, method="multi")

print("Loading accounts...")
accounts = pd.read_csv("hayag.csv")
accounts = accounts.rename(columns={
    "type": "account_type"
})
accounts.to_sql("accounts", engine, if_exists="append", index=False, method="multi")

print("Loading loans...")
loans = pd.read_csv("zeel.csv")
loans = loans.rename(columns={
    "amount": "loan_amount"
})
loans.to_sql("loans", engine, if_exists="append", index=False, method="multi")

print("Loading transactions...")
for chunk in pd.read_csv("guilgee.csv", chunksize=50000):
    chunk = chunk.rename(columns={
        "type": "transaction_type",
        "date": "transaction_date"
    })

    chunk.to_sql("transactions", engine, if_exists="append", index=False, method="multi")
    print(f"{len(chunk)} rows inserted")

print("ETL Completed Successfully!")