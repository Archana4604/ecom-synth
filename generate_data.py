# generate_data.py
import csv, random, os
from datetime import datetime, timedelta

random.seed(42)
NUM_CUSTOMERS = 200
NUM_PRODUCTS = 100
NUM_ORDERS = 500

def rand_date(start_year=2021, end_year=2025):
    start = datetime(start_year,1,1)
    end = datetime(end_year,12,31)
    delta = (end - start).days
    return (start + timedelta(days=random.randint(0, delta))).date().isoformat()

first_names = ["Aditi","Rahul","Priya","Karan","Neha","Vikram","Sana","Rohit","Anita","Manish","Archana","Deepa"]
last_names = ["Sharma","Patel","Kumar","Singh","Gupta","Iyer","Reddy","Nair","Verma","Bose"]
countries = ["India","USA","UK","Canada","Australia","Germany"]
categories = ["Electronics","Home","Books","Clothing","Toys","Beauty"]
warehouses = ["WH-A", "WH-B", "WH-C"]

customers=[]
for cid in range(1, NUM_CUSTOMERS+1):
    fn = random.choice(first_names); ln = random.choice(last_names)
    email = f"{fn.lower()}.{ln.lower()}{cid}@example.com"
    signup = rand_date(2019,2025)
    customers.append([cid, fn, ln, email, signup, random.choice(countries)])

products=[]
for pid in range(1, NUM_PRODUCTS+1):
    sku = f"SKU{10000+pid}"
    name = f"{random.choice(['Pro','Ultra','Smart','Eco','Classic','Mini'])} {random.choice(['Widget','Gadget','Item','Device'])} {pid}"
    category = random.choice(categories)
    price = round(random.uniform(5.0, 500.0), 2)
    products.append([pid, sku, name, category, price])

inventory=[]
for pid, *_ in products:
    stock = random.randint(0,500)
    restock = rand_date(2024,2025) if stock < 20 else ""
    inventory.append([pid, random.choice(warehouses), stock, restock])

orders=[]
order_items=[]
order_item_id = 1
for oid in range(1, NUM_ORDERS+1):
    cust = random.randint(1, NUM_CUSTOMERS)
    order_date = rand_date(2022,2025)
    status = random.choices(["completed","cancelled","refunded","pending"], weights=[0.75,0.1,0.05,0.1])[0]
    n_items = random.randint(1,4)
    chosen = random.sample(range(1, NUM_PRODUCTS+1), n_items)
    total = 0.0
    for pid in chosen:
        qty = random.randint(1,5)
        price = next(p[4] for p in products if p[0]==pid)
        total += price * qty
        order_items.append([order_item_id, oid, pid, qty, price])
        order_item_id += 1
    total = round(total,2)
    orders.append([oid, cust, order_date, total, status])

os.makedirs("data", exist_ok=True)
with open("data/customers.csv","w",newline="") as f:
    writer=csv.writer(f); writer.writerow(["customer_id","first_name","last_name","email","signup_date","country"]); writer.writerows(customers)
with open("data/products.csv","w",newline="") as f:
    writer=csv.writer(f); writer.writerow(["product_id","sku","name","category","price"]); writer.writerows(products)
with open("data/inventory.csv","w",newline="") as f:
    writer=csv.writer(f); writer.writerow(["product_id","warehouse","stock_qty","restock_date"]); writer.writerows(inventory)
with open("data/orders.csv","w",newline="") as f:
    writer=csv.writer(f); writer.writerow(["order_id","customer_id","order_date","total_amount","status"]); writer.writerows(orders)
with open("data/order_items.csv","w",newline="") as f:
    writer=csv.writer(f); writer.writerow(["order_item_id","order_id","product_id","quantity","unit_price"]); writer.writerows(order_items)

print("Generated files in data/:",
      f"customers={len(customers)} products={len(products)} orders={len(orders)} order_items={len(order_items)} inventory={len(inventory)}")
