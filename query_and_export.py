# query_and_export.py
import sqlite3, csv, os
DB="ecom.db"
OUT="output"
os.makedirs(OUT, exist_ok=True)

QUERY = """
SELECT
  o.order_id, o.order_date, o.status,
  c.customer_id, (c.first_name || ' ' || c.last_name) AS customer_name,
  oi.product_id, p.name AS product_name, p.sku, p.category,
  oi.quantity, oi.unit_price, (oi.quantity * oi.unit_price) AS line_total,
  o.total_amount AS order_total
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
WHERE o.status = 'completed'
  AND o.order_date BETWEEN '2024-01-01' AND '2025-12-31'
ORDER BY o.order_date DESC, o.order_id ASC
LIMIT 1000;
"""

def run():
    conn=sqlite3.connect(DB)
    cur=conn.cursor()
    cur.execute(QUERY)
    cols=[d[0] for d in cur.description]
    rows=cur.fetchall()
    out_path=os.path.join(OUT,"order_lines.csv")
    with open(out_path,"w",newline="") as f:
        w=csv.writer(f); w.writerow(cols); w.writerows(rows)
    print(f"Exported {len(rows)} rows -> {out_path}")
    for r in rows[:5]: print(r)
    conn.close()

if __name__=="__main__":
    run()
