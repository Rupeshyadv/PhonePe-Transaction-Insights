import os
import json
from db_connection import get_connection

BASE_PATH = "../data/map"

conn = get_connection()


# COMMON PROCESSOR
def process_map(base_path, data_type):
    rows = []

    for state in os.listdir(base_path):
        state_path = os.path.join(base_path, state)

        if not os.path.isdir(state_path):
            continue

        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)

            if not year.isdigit():
                continue

            for file in os.listdir(year_path):
                if not file.endswith(".json"):
                    continue

                quarter = int(file.replace(".json", ""))

                with open(os.path.join(year_path, file)) as f:
                    data = json.load(f)

                rows.extend(extract_map_data(data, state, year, quarter, data_type))

    return rows


# EXTRACTOR
def extract_map_data(data, state, year, quarter, data_type):
    rows = []

    if not data.get("data"):
        return rows

    # TRANSACTION & INSURANCE 
    if data_type in ["transaction", "insurance"]:
        if not data["data"].get("hoverDataList"):
            return rows

        for item in data["data"]["hoverDataList"]:
            rows.append((
                state,
                item.get("name"),  # district
                int(year),
                quarter,
                item.get("metric")[0].get("count", 0),
                item.get("metric")[0].get("amount", 0)
            ))

    # USER
    elif data_type == "user":
        if not data["data"].get("hoverData"):
            return rows

        for district, values in data["data"]["hoverData"].items():
            rows.append((
                state,
                district,
                int(year),
                quarter,
                values.get("registeredUsers", 0),
                values.get("appOpens", 0)
            ))

    return rows


# LOADERS

def load_map_transaction():
    rows = process_map(
        os.path.join(BASE_PATH, "transaction/hover/country/india/state"),
        "transaction"
    )

    query = """
    INSERT INTO map_transaction
    (state, district, year, quarter, transaction_count, transaction_amount)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor = conn.cursor()
    cursor.executemany(query, rows)
    conn.commit()
    cursor.close()

    print("✅ Map Transaction Loaded")


def load_map_insurance():
    rows = process_map(
        os.path.join(BASE_PATH, "insurance/country/india/state"),
        "insurance"
    )

    query = """
    INSERT INTO map_insurance
    (state, district, year, quarter, transaction_count, transaction_amount)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor = conn.cursor()
    cursor.executemany(query, rows)
    conn.commit()
    cursor.close()

    print("✅ Map Insurance Loaded")


def load_map_user():
    rows = process_map(
        os.path.join(BASE_PATH, "user/hover/country/india/state"),
        "user"
    )

    query = """
    INSERT INTO map_user
    (state, district, year, quarter, registered_users, app_opens)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor = conn.cursor()
    cursor.executemany(query, rows)
    conn.commit()
    cursor.close()

    print("✅ Map User Loaded")


# RUN
if __name__ == "__main__":
    load_map_transaction()
    load_map_insurance()
    load_map_user()

    conn.close()

    print("🚀 ALL MAP DATA LOADED")