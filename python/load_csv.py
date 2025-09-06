import csv
import mysql.connector
from datetime import datetime

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",       
    database="storedb"
)
cur = conn.cursor()


def to_int(x):
    return int(x) if x and x.strip() != "" else None

def to_float(x):
    return float(x) if x and x.strip() != "" else None

def to_date(x):
    if not x or x.strip() == "":
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(x.strip(), fmt).date()
        except ValueError:
            pass
    return None

expected = ["OrderID","CustomerID","Category","Quantity","UnitPrice",
            "TotalAmount","PaymentMethod","Region","OrderDate"]

bad_rows = 0
batch = []
line_no = 1  

with open("pboutique_sales.csv", newline="", encoding="utf-8") as f:
    rdr = csv.DictReader(f)
    missing = [k for k in expected if k not in rdr.fieldnames]
    if missing:
        raise RuntimeError(f"CSV missing columns: {missing}. Found: {rdr.fieldnames}")

    for line_no, r in enumerate(rdr, start=2):  
        try:
            row = (
                r["OrderID"],
                r["CustomerID"],
                r["Category"],
                to_int(r["Quantity"]),
                to_float(r["UnitPrice"]),
                to_float(r["TotalAmount"]),
                r["PaymentMethod"],
                r["Region"],
                to_date(r["OrderDate"]),
            )

            if len(row) != 9:
                raise ValueError(f"param count {len(row)} != 9")

            batch.append(row)

        except Exception as e:
            bad_rows += 1
            if bad_rows <= 5:
                print(f"[WARN] Skipping line {line_no}: {e} | data={r}")

sql = """
INSERT INTO orders
(OrderID, CustomerID, Category, Quantity, UnitPrice, TotalAmount, PaymentMethod, Region, OrderDate)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""
if batch:
    cur.executemany(sql, batch)
    conn.commit()

print(f"Inserted {cur.rowcount} rows. Skipped {bad_rows} bad row(s).")

cur.close()
conn.close()
