
from faker import Faker
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from tqdm import tqdm

fake = Faker()

# =====================================================
# CONFIG (dynamic realistic sizes)
# =====================================================
np.random.seed(None)

MAX_CUSTOMERS = 150_000

N_CUSTOMERS = np.random.randint(140_000, MAX_CUSTOMERS + 1)
N_ACCOUNTS = int(N_CUSTOMERS * np.random.uniform(1.3, 1.6))
N_LOANS = int(N_CUSTOMERS * np.random.uniform(0.35, 0.55))
N_TRANSACTIONS = int(N_ACCOUNTS * np.random.uniform(6, 10))

TODAY = datetime.now().date()

print("="*50)
print(f"Customers: {N_CUSTOMERS:,}")
print(f"Accounts : {N_ACCOUNTS:,}")
print(f"Loans    : {N_LOANS:,}")
print(f"Txns     : {N_TRANSACTIONS:,}")
print("="*50)

# =====================================================
# HELPERS
# =====================================================

def zipf_weights(n, s=1.2):
    ranks = np.arange(1, n + 1)
    w = 1 / np.power(ranks, s)
    return w / w.sum()

def generate_dates(n, start, end, growth=0.0008, seasonal=False):
    days = (end - start).days
    idx = np.arange(days + 1)

    w = np.exp(growth * idx)

    if seasonal:
        dates = np.array([start + timedelta(days=int(i)) for i in idx])
        m = np.array([d.month for d in dates])
        wd = np.array([d.weekday() for d in dates])

        season = np.select(
            [m==12, m==1, np.isin(m,[6,7])],
            [1.6, 1.3, 0.7],
            default=1.0
        )
        weekend = np.where(wd>=5, 0.5, 1.0)

        w = w * season * weekend

    w = w / w.sum()
    pick = np.random.choice(idx, size=n, p=w)
    return [start + timedelta(days=int(i)) for i in pick]

# =====================================================
# CUSTOMERS
# =====================================================

print("Generating customers...")

cities = [fake.city() for _ in range(20)]
city_w = zipf_weights(20)

ages = np.clip(np.random.normal(38, 14, N_CUSTOMERS), 18, 80).astype(int)

customers = pd.DataFrame({
    "customer_id": np.arange(1, N_CUSTOMERS+1),
    "name": [fake.name() for _ in tqdm(range(N_CUSTOMERS))],
    "age": ages,
    "gender": np.random.choice(["M","F"], N_CUSTOMERS),
    "city": np.random.choice(cities, N_CUSTOMERS, p=city_w),
    "register_date": generate_dates(
        N_CUSTOMERS,
        datetime.now().date() - timedelta(days=5*365),
        TODAY
    )
})

customers.to_csv("customers.csv", index=False)

# =====================================================
# ACCOUNTS
# =====================================================

print("Generating accounts...")

acc_types = ["Savings","Current","Salary"]
acc_p = [0.45,0.35,0.2]

acc_type = np.random.choice(acc_types, N_ACCOUNTS, p=acc_p)

mu = {"Savings":13.6,"Current":13.3,"Salary":12.8}
sigma = {"Savings":1.3,"Current":1.1,"Salary":0.9}

balances = np.zeros(N_ACCOUNTS)

for t in acc_types:
    m = acc_type == t
    balances[m] = np.random.lognormal(mu[t], sigma[t], m.sum())

accounts = pd.DataFrame({
    "account_id": np.arange(1, N_ACCOUNTS+1),
    "customer_id": np.random.randint(1, N_CUSTOMERS+1, N_ACCOUNTS),
    "type": acc_type,
    "balance": balances.round(2)
})

accounts.to_csv("accounts.csv", index=False)

# =====================================================
# LOANS
# =====================================================

print("Generating loans...")

status = np.random.choice(["Active","Closed","Default"], N_LOANS, p=[0.55,0.3,0.15])

loan_amt = np.random.lognormal(16,1.0,N_LOANS)
rate = np.random.normal(14,3,N_LOANS) + np.where(status=="Default", np.random.uniform(2,6,N_LOANS),0)

loans = pd.DataFrame({
    "loan_id": np.arange(1, N_LOANS+1),
    "customer_id": np.random.randint(1, N_CUSTOMERS+1, N_LOANS),
    "amount": loan_amt,
    "interest_rate": np.clip(rate,8,24),
    "status": status
})

loans.to_csv("loans.csv", index=False)

# =====================================================
# TRANSACTIONS
# =====================================================

print("Generating transactions...")

types = ["Deposit","Withdrawal","Transfer","Payment"]
tp = [0.35,0.3,0.2,0.15]

mu_t = {"Deposit":11.5,"Withdrawal":11.2,"Transfer":12,"Payment":11}
sg_t = {"Deposit":1.0,"Withdrawal":1.0,"Transfer":1.3,"Payment":0.9}

batch = 100000
batches = (N_TRANSACTIONS + batch - 1)//batch

for b in range(batches):
    n = min(batch, N_TRANSACTIONS - b*batch)

    t = np.random.choice(types, n, p=tp)

    amt = np.zeros(n)
    for x in types:
        m = t == x
        amt[m] = np.random.lognormal(mu_t[x], sg_t[x], m.sum())

    dates = generate_dates(
        n,
        datetime.now().date() - timedelta(days=3*365),
        TODAY,
        seasonal=True
    )

    df = pd.DataFrame({
        "transaction_id": np.arange(b*batch+1, b*batch+n+1),
        "account_id": np.random.randint(1, N_ACCOUNTS+1, n),
        "type": t,
        "amount": amt.round(2),
        "date": dates
    })

    df.to_csv("transactions.csv", index=False if b==0 else True, mode="w" if b==0 else "a", header=b==0)

    print(f"Batch {b+1}/{batches} done")

print("DONE")
