import os
import json
from db_connection import get_connection

BASE_PATH = "../data/top"

conn = get_connection()


# COMMON PROCESSOR
def process_top(base_path, data_type):
    rows = []

    for year in os.listdir(base_path):
        year_path = os.path.join(base_path, year)

        if not year.isdigit():
            continue

        for file in os.listdir(year_path):
            if not file.endswith(".json"):
                continue

            quarter = int(file.replace(".json", ""))

            with open(os.path.join(year_path, file)) as f:
                data = json.load(f)

            rows.extend(extract_top_data(data, year, quarter, data_type))

    return rows

def get_metrics(item):
    metric = item.get("metric", {})

    # case 1: list
    if isinstance(metric, list):
        metric = metric[0] if metric else {}

    # case 2: dict
    if isinstance(metric, dict):
        return metric.get("count", 0), metric.get("amount", 0)

    return 0, 0

# EXTRACTOR
def extract_top_data(data, year, quarter, data_type):
    rows = []

    if not data.get("data"):
        return rows

    d = data["data"]

    # STATES
    for item in d.get("states", []):
        count, amount = get_metrics(item)
        
        rows.append((
            item.get("name"),
            None,
            None,
            int(year),
            quarter,
            count,
            amount
        ))

    # DISTRICTS
    for item in d.get("districts", []):
        count, amount = get_metrics(item)
        
        rows.append((
            None,
            item.get("name"),
            None,
            int(year),
            quarter,
            count,
            amount
        ))

    # PINCODES
    for item in d.get("pincodes", []):
        count, amount = get_metrics(item)
        
        rows.append((
            None,
            None,
            item.get("name"),
            int(year),
            quarter,
            count,
            amount
        ))

    return rows


# LOADERS

def load_top_transaction():
    rows = process_top(
        os.path.join(BASE_PATH, "transaction/country/india"),
        "transaction"
    )

    query = """
    INSERT INTO top_transaction
    (state, district, pincode, year, quarter, transaction_count, transaction_amount)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor = conn.cursor()
    cursor.executemany(query, rows)
    conn.commit()
    cursor.close()

    print("✅ Top Transaction Loaded")


def load_top_insurance():
    rows = process_top(
        os.path.join(BASE_PATH, "insurance/country/india"),
        "insurance"
    )

    query = """
    INSERT INTO top_insurance
    (state, district, pincode, year, quarter, transaction_count, transaction_amount)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor = conn.cursor()
    cursor.executemany(query, rows)
    conn.commit()
    cursor.close()

    print("✅ Top Insurance Loaded")


def load_top_user():
    rows = process_top(
        os.path.join(BASE_PATH, "user/country/india"),
        "user"
    )

    query = """
    INSERT INTO top_user
    (state, district, pincode, year, quarter, registered_users)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    # user doesn't have amount → adjust
    user_rows = [(r[0], r[1], r[2], r[3], r[4], r[5]) for r in rows]

    cursor = conn.cursor()
    cursor.executemany(query, user_rows)
    conn.commit()
    cursor.close()

    print("✅ Top User Loaded")


# RUN
if __name__ == "__main__":
    load_top_transaction()
    load_top_insurance()
    load_top_user()

    conn.close()

    print("🚀 ALL TOP DATA LOADED")