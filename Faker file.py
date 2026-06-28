from faker import Faker
import pandas as pd
import random
from datetime import datetime
from tqdm import tqdm

fake = Faker()

# ====================================
# CUSTOMERS (100,000)
# ====================================

customers = []

for customer_id in tqdm(range(1, 100001), desc="Customers"):
    customers.append({
        "customer_id": customer_id,
        "name": fake.name(),
        "gender": random.choice(["Male", "Female"]),
        "age": random.randint(18, 80),
        "city": fake.city(),
        "register_date": fake.date_between(
            start_date='-5y',
            end_date='today'
        )
    })

customers_df = pd.DataFrame(customers)
customers_df.to_csv("customers.csv", index=False)

print("Customers created")


# ====================================
# ACCOUNTS (150,000)
# ====================================

account_types = [
    "Savings",
    "Current",
    "Salary"
]

accounts = []

for account_id in tqdm(range(1, 150001), desc="Accounts"):
    accounts.append({
        "account_id": account_id,
        "customer_id": random.randint(1, 100000),
        "account_type": random.choice(account_types),
        "balance": round(random.uniform(100, 50000000), 2)
    })

accounts_df = pd.DataFrame(accounts)
accounts_df.to_csv("accounts.csv", index=False)

print("Accounts created")


# ====================================
# LOANS (50,000)
# ====================================

loan_statuses = [
    "Active",
    "Closed",
    "Defaulted"
]

loans = []

for loan_id in tqdm(range(1, 50001), desc="Loans"):
    loans.append({
        "loan_id": loan_id,
        "customer_id": random.randint(1, 100000),
        "loan_amount": round(random.uniform(1000000, 100000000), 2),
        "interest_rate": round(random.uniform(8, 24), 2),
        "status": random.choice(loan_statuses)
    })

loans_df = pd.DataFrame(loans)
loans_df.to_csv("loans.csv", index=False)

print("Loans created")


# ====================================
# TRANSACTIONS (1,000,000)
# ====================================

transaction_types = [
    "Deposit",
    "Withdrawal",
    "Transfer",
    "Payment"
]

batch_size = 100000

for batch in range(10):

    transactions = []

    start_id = batch * batch_size + 1
    end_id = start_id + batch_size

    for transaction_id in tqdm(
            range(start_id, end_id),
            desc=f"Batch {batch+1}/10"):

        transactions.append({
            "transaction_id": transaction_id,
            "account_id": random.randint(1, 150000),
            "amount": round(random.uniform(1000, 5000000), 2),
            "transaction_date": fake.date_between(
                start_date='-3y',
                end_date='today'
            ),
            "type": random.choice(transaction_types)
        })

    batch_df = pd.DataFrame(transactions)

    if batch == 0:
        batch_df.to_csv(
            "transactions.csv",
            mode="w",
            header=True,
            index=False
        )
    else:
        batch_df.to_csv(
            "transactions.csv",
            mode="a",
            header=False,
            index=False
        )

    print(f"Batch {batch+1} completed")

print("Transactions created")
print("All files generated successfully")