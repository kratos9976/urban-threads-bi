"""
Step 2 — Synthetic dataset generator for Urban Threads.
Generates: stores, products, customers, orders, order_items, inventory, returns, discounts
Output: CSV files in data/raw/
No external dependencies beyond pandas/numpy.
"""
import random
from datetime import date, timedelta
import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

OUT_DIR = "data/raw"
START_DATE = date(2024, 1, 1)
END_DATE = date(2025, 12, 31)
N_CUSTOMERS = 2000
N_PRODUCTS = 150
N_ORDERS = 8000

FIRST_NAMES = ["Olivia", "Jack", "Charlotte", "William", "Amelia", "Noah", "Ava", "Thomas",
               "Isla", "James", "Mia", "Oliver", "Grace", "Lucas", "Chloe", "Henry", "Zoe",
               "Ethan", "Ruby", "Alexander", "Sophie", "Liam", "Emily", "Jacob", "Ella"]
LAST_NAMES = ["Smith", "Jones", "Williams", "Brown", "Wilson", "Taylor", "Nguyen", "Lee",
              "Chen", "Kelly", "Walker", "Robinson", "Clarke", "Mitchell", "Campbell",
              "Anderson", "Stewart", "Murphy", "Cook", "Bell"]
WORDS = ["Harbour", "Aster", "Nova", "Cedar", "Vale", "Fable", "Marlow", "Wren",
         "Dune", "Reed", "Ember", "Sable", "Quill", "Birch", "Cove"]

def rand_date(start, end):
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))

def rand_email(first, last, seen):
    base = f"{first.lower()}.{last.lower()}"
    email = f"{base}@example.com"
    i = 1
    while email in seen:
        email = f"{base}{i}@example.com"
        i += 1
    seen.add(email)
    return email

# ---------- Stores ----------
stores = pd.DataFrame([
    {"store_id": 1, "store_name": "Urban Threads Melbourne CBD", "city": "Melbourne", "channel": "Store"},
    {"store_id": 2, "store_name": "Urban Threads Sydney CBD", "city": "Sydney", "channel": "Store"},
    {"store_id": 3, "store_name": "Urban Threads Brisbane", "city": "Brisbane", "channel": "Store"},
    {"store_id": 4, "store_name": "Urban Threads Perth", "city": "Perth", "channel": "Store"},
    {"store_id": 5, "store_name": "Urban Threads Adelaide", "city": "Adelaide", "channel": "Store"},
    {"store_id": 6, "store_name": "Urban Threads Online", "city": "Online", "channel": "Online"},
])
stores.to_csv(f"{OUT_DIR}/stores.csv", index=False)

# ---------- Products ----------
categories = {
    "Menswear": ["Shirt", "Jeans", "Jacket", "T-Shirt", "Chinos"],
    "Womenswear": ["Dress", "Blouse", "Skirt", "Jeans", "Cardigan"],
    "Footwear": ["Sneakers", "Boots", "Sandals", "Loafers"],
    "Accessories": ["Belt", "Scarf", "Cap", "Sunglasses", "Bag"],
}
products = []
pid = 1
for cat, items in categories.items():
    for _ in range(N_PRODUCTS // len(categories)):
        item = random.choice(items)
        cost = round(random.uniform(8, 60), 2)
        margin = random.uniform(1.8, 3.2)
        products.append({
            "product_id": pid,
            "product_name": f"{random.choice(WORDS)} {item}",
            "category": cat,
            "cost_price": cost,
            "sale_price": round(cost * margin, 2),
        })
        pid += 1
products = pd.DataFrame(products)
products.to_csv(f"{OUT_DIR}/products.csv", index=False)

# ---------- Customers ----------
segments = ["New", "Regular", "VIP", "Lapsed"]
seg_weights = [0.35, 0.4, 0.15, 0.1]
customers = []
seen_emails = set()
for cid in range(1, N_CUSTOMERS + 1):
    first, last = random.choice(FIRST_NAMES), random.choice(LAST_NAMES)
    signup = rand_date(START_DATE, END_DATE)
    customers.append({
        "customer_id": cid,
        "first_name": first,
        "last_name": last,
        "email": rand_email(first, last, seen_emails),
        "city": random.choice(["Melbourne", "Sydney", "Brisbane", "Perth", "Adelaide", "Other"]),
        "signup_date": signup,
        "segment": random.choices(segments, weights=seg_weights)[0],
    })
customers = pd.DataFrame(customers)
customers.to_csv(f"{OUT_DIR}/customers.csv", index=False)

# ---------- Orders + Order Items ----------
orders, order_items = [], []
oid, oiid = 1, 1
melbourne_decline_start = date(2025, 7, 1)  # deliberate dip -> Step 7 AI explains this later

store_weights = [0.16, 0.16, 0.14, 0.13, 0.13, 0.28]
for _ in range(N_ORDERS):
    order_date = rand_date(START_DATE, END_DATE)
    store = stores.sample(1, weights=store_weights).iloc[0]

    if store["city"] == "Melbourne" and order_date >= melbourne_decline_start:
        if random.random() < 0.45:
            continue

    cust = customers.sample(1).iloc[0]
    n_items = random.choices([1, 2, 3, 4], weights=[0.5, 0.3, 0.15, 0.05])[0]
    order_items_sample = products.sample(n_items)

    order_total = 0
    for _, prod in order_items_sample.iterrows():
        qty = random.choices([1, 2, 3], weights=[0.7, 0.2, 0.1])[0]
        line_total = round(prod["sale_price"] * qty, 2)
        order_total += line_total
        order_items.append({
            "order_item_id": oiid,
            "order_id": oid,
            "product_id": prod["product_id"],
            "quantity": qty,
            "unit_price": prod["sale_price"],
            "line_total": line_total,
        })
        oiid += 1

    orders.append({
        "order_id": oid,
        "customer_id": cust["customer_id"],
        "store_id": store["store_id"],
        "order_date": order_date,
        "channel": store["channel"],
        "order_total": round(order_total, 2),
    })
    oid += 1

orders = pd.DataFrame(orders)
order_items = pd.DataFrame(order_items)
orders.to_csv(f"{OUT_DIR}/orders.csv", index=False)
order_items.to_csv(f"{OUT_DIR}/order_items.csv", index=False)

# ---------- Inventory ----------
inventory = []
inv_id = 1
for _, store in stores.iterrows():
    for _, prod in products.sample(frac=0.8).iterrows():
        stock = np.random.poisson(lam=25)
        inventory.append({
            "inventory_id": inv_id,
            "store_id": store["store_id"],
            "product_id": prod["product_id"],
            "stock_on_hand": stock,
            "reorder_level": 10,
            "snapshot_date": END_DATE,
        })
        inv_id += 1
inventory = pd.DataFrame(inventory)
inventory.to_csv(f"{OUT_DIR}/inventory.csv", index=False)

# ---------- Returns ----------
return_reasons = ["Wrong size", "Changed mind", "Damaged/faulty", "Not as described", "Late delivery"]
returns = []
rid = 1
returnable_items = order_items.sample(frac=0.09)
orders_indexed = orders.set_index("order_id")
for _, item in returnable_items.iterrows():
    order_date = orders_indexed.loc[item["order_id"], "order_date"]
    return_date = order_date + timedelta(days=random.randint(2, 21))
    returns.append({
        "return_id": rid,
        "order_id": item["order_id"],
        "order_item_id": item["order_item_id"],
        "return_date": return_date,
        "reason": random.choices(return_reasons, weights=[0.35, 0.25, 0.2, 0.1, 0.1])[0],
        "refund_amount": item["line_total"],
    })
    rid += 1
returns = pd.DataFrame(returns)
returns["order_id"] = returns["order_id"].astype(int)
returns["order_item_id"] = returns["order_item_id"].astype(int)
returns.to_csv(f"{OUT_DIR}/returns.csv", index=False)

# ---------- Discounts ----------
discount_campaigns = [
    ("SUMMER24", date(2024, 12, 1), date(2025, 1, 15), 0.20),
    ("EOFY24", date(2024, 6, 15), date(2024, 6, 30), 0.25),
    ("VIP_EXCLUSIVE", date(2025, 3, 1), date(2025, 3, 31), 0.15),
    ("BLACKFRIDAY24", date(2024, 11, 25), date(2024, 11, 29), 0.30),
    ("WINTER25", date(2025, 6, 1), date(2025, 7, 31), 0.20),
]
discounts = pd.DataFrame([
    {"campaign_code": c, "start_date": s, "end_date": e, "discount_pct": p}
    for c, s, e, p in discount_campaigns
])
discounts.to_csv(f"{OUT_DIR}/discounts.csv", index=False)

print("Done. Rows generated:")
for name, df in [("stores", stores), ("products", products), ("customers", customers),
                  ("orders", orders), ("order_items", order_items), ("inventory", inventory),
                  ("returns", returns), ("discounts", discounts)]:
    print(f"  {name}: {len(df)}")
