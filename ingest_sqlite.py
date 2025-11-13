# ingest_sqlite.py
import sqlite3, csv, os
DB="ecom.db"
DATA_DIR="data"

SCHEMA = {
    "customers": """
        CREATE TABLE IF NOT EXISTS customers(
            customer_id INTEGER PRIMARY KEY,
            first_name TEXT, last_name TEXT, email TEXT, signup_date TEXT, country TEXT
        );
    """,
    "products": """
        CREATE TABLE IF NOT EXISTS products(
            product_id INTEGER PRIMARY KEY, sku TEXT, name TEXT, category TEXT, price REAL
        );
    """,
    "inventory": """
        CREATE TABLE IF NOT EXISTS inventory(
            product_id INTEGER, warehouse TEXT, stock_qty INTEGER, restock_date TEXT,
            PRIMARY KEY(product_id, warehouse),
            FOREIGN KEY(product_id) REFERENCES products(product_id)
        );
    """,
    "orders": """
        CREATE TABLE IF NOT EXISTS orders(
            order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, total_amount REAL, status TEXT,
            FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
        );
    """,
    "order_items": """
        CREATE TABLE IF NOT EXISTS order_items(
            order_item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, quantity INTEGER, unit_price REAL,
            FOREIGN KEY(order_id) REFERENCES orders(order_id),
            FOREIGN KEY(product_id) REFERENCES products(product_id)
        );
    """
}

def import_csv(conn, path, table, cols):
    cur=conn.cursor()
    with open(path,newline="") as f:
        reader=csv.DictReader(f)
        rows=[tuple(row[c] for c in cols) for row in reader]
    placeholders=",".join("?" for _ in cols)
    cur.executemany(f"INSERT INTO {table} ({','.join(cols)}) VALUES ({placeholders})", rows)
    conn.commit()
    print(f"Inserted {len(rows)} rows into {table}")

def main():
    if not os.path.isdir(DATA_DIR):
        raise SystemExit("Run generate_data.py first")
    conn=sqlite3.connect(DB)
    cur=conn.cursor()
    for ddl in SCHEMA.values(): cur.execute(ddl)
    conn.commit()
    import_csv(conn, os.path.join(DATA_DIR,"customers.csv"), "customers", ["customer_id","first_name","last_name","email","signup_date","country"])
    import_csv(conn, os.path.join(DATA_DIR,"products.csv"), "products", ["product_id","sku","name","category","price"])
    import_csv(conn, os.path.join(DATA_DIR,"inventory.csv"), "inventory", ["product_id","warehouse","stock_qty","restock_date"])
    import_csv(conn, os.path.join(DATA_DIR,"orders.csv"), "orders", ["order_id","customer_id","order_date","total_amount","status"])
    import_csv(conn, os.path.join(DATA_DIR,"order_items.csv"), "order_items", ["order_item_id","order_id","product_id","quantity","unit_price"])
    conn.close()
    print("DB created: ecom.db")

if __name__=="__main__":
    main()
