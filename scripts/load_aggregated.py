import os
import json
from db_connection import get_connection

BASE_PATH = "../data/aggregated/"

conn = get_connection()
cursor = conn.cursor()

def process_aggregated(base_path, data_type):
    rows = []

    # COUNTRY LEVEL
    for year in os.listdir(base_path):
        year_path = os.path.join(base_path, year)

        if not year.isdigit() or not os.path.isdir(year_path):
            continue

        for file in os.listdir(year_path):
            if not file.endswith(".json"):
                continue

            quarter = int(file.replace(".json", ""))

            with open(os.path.join(year_path, file)) as f:
                data = json.load(f)

            rows.extend(extract_data(data, "India", year, quarter, data_type))

    # STATE LEVEL
    state_path = os.path.join(base_path, "state")

    if os.path.exists(state_path):
        for state in os.listdir(state_path):
            state_folder = os.path.join(state_path, state)

            for year in os.listdir(state_folder):
                year_path = os.path.join(state_folder, year)

                if not year.isdigit() or not os.path.isdir(year_path):
                    continue

                for file in os.listdir(year_path):
                    if not file.endswith(".json"):
                        continue

                    quarter = int(file.replace(".json", ""))

                    with open(os.path.join(year_path, file)) as f:
                        data = json.load(f)

                    rows.extend(extract_data(data, state, year, quarter, data_type))

    return rows


# 🔥 EXTRACTOR (handles different JSON formats)
def extract_data(data, state, year, quarter, data_type):
    rows = []

    if not data.get("data"):
        return rows

    # TRANSACTION & INSURANCE
    if data_type in ["transaction", "insurance"]:
        if not data["data"].get("transactionData"):
            return rows

        for item in data["data"]["transactionData"]:
            for inst in item.get("paymentInstruments", []):
                rows.append((
                    state,
                    int(year),
                    quarter,
                    item.get("name"),
                    inst.get("count", 0),
                    inst.get("amount", 0)
                ))

    # USER
    elif data_type == "user":
        if not data["data"].get("usersByDevice"):
            return rows

        for item in data["data"]["usersByDevice"]:
            rows.append((
                state,
                int(year),
                quarter,
                item.get("brand"),
                item.get("count", 0),
                item.get("percentage", 0)
            ))

    return rows


# LOADERS
def load_aggregated_transaction():
    rows = process_aggregated(
        os.path.join(BASE_PATH, "transaction/country/india"),
        "transaction"
    )

    query = """
    INSERT INTO aggregated_transaction
    (state, year, quarter, transaction_type, transaction_count, transaction_amount)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor = conn.cursor()
    cursor.executemany(query, rows)
    conn.commit()
    cursor.close()
    print("✅ Aggregated Transaction Loaded")


def load_aggregated_insurance():
    rows = process_aggregated(
        os.path.join(BASE_PATH, "insurance/country/india"),
        "insurance"
    )

    query = """
    INSERT INTO aggregated_insurance
    (state, year, quarter, insurance_type, transaction_count, transaction_amount)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor = conn.cursor()
    cursor.executemany(query, rows)
    conn.commit()
    cursor.close()
    print("✅ Aggregated Insurance Loaded")


def load_aggregated_user():
    rows = process_aggregated(
        os.path.join(BASE_PATH, "user/country/india"),
        "user"
    )

    query = """
    INSERT INTO aggregated_user
    (state, year, quarter, brand, user_count, percentage)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor = conn.cursor()
    cursor.executemany(query, rows)
    conn.commit()
    cursor.close()           
    print("✅ Aggregated User Loaded")


if __name__ == "__main__":
    load_aggregated_transaction()
    load_aggregated_insurance()
    load_aggregated_user()
    
    conn.close()

    print("🚀 ALL AGGREGATED DATA LOADED")