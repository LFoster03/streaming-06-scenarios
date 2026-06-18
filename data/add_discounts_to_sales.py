"""add_discounts_to_sales.py.

Adds discount codes to sales.csv based on simple rules:
  - TEAM20  : quantity >= 3 (team purchase discount)
  - WELCOME10: is_new_customer == true (new customer welcome discount)
  - SUMMER15 : ~20% of remaining rows (random summer promotion)

Run from the root project folder:
    uv run python add_discounts_to_sales.py
"""

import csv
from pathlib import Path
import random

# === PATHS ===
DATA_DIR = Path("data")
SALES_CSV = DATA_DIR / "sales.csv"
BACKUP_CSV = DATA_DIR / "sales_backup.csv"

# === SETTINGS ===
SUMMER15_PROBABILITY = 0.2  # 20% chance for remaining rows
RANDOM_SEED = 42  # for reproducibility

random.seed(RANDOM_SEED)

# === BACKUP ORIGINAL ===
if not BACKUP_CSV.exists():
    BACKUP_CSV.write_bytes(SALES_CSV.read_bytes())
    print(f"Backup saved to {BACKUP_CSV}")
else:
    print(f"Backup already exists at {BACKUP_CSV}, skipping.")

# === READ, MODIFY, WRITE ===
rows = list(csv.DictReader(SALES_CSV.open(newline="")))

assigned = 0
for row in rows:
    # Skip rows that already have a discount code
    if row.get("discount_code", "").strip():
        continue

    quantity = int(row.get("quantity", 0))
    is_new_customer = row.get("is_new_customer", "").strip().lower()

    if quantity >= 3:
        row["discount_code"] = "TEAM20"
        assigned += 1
    elif is_new_customer == "true":
        row["discount_code"] = "WELCOME10"
        assigned += 1
    elif random.random() < SUMMER15_PROBABILITY:
        row["discount_code"] = "SUMMER15"
        assigned += 1

# === WRITE UPDATED CSV ===
fieldnames = list(rows[0].keys())
with SALES_CSV.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Done! Assigned discount codes to {assigned} rows in {SALES_CSV}")
