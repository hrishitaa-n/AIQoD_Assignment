import os
from datetime import datetime
from pathlib import Path

import pandas as pd
from pymongo import MongoClient, ASCENDING

from config import MONGO_URI, CSV_PATH, log
# MongoDB


def get_db():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        log.info("Connected to MongoDB")
        return client["product_db"]
    except Exception as e:
        log.error("MongoDB connection failed: %s", e)
        log.error("See if MongoDB is running: net start MongoDB")
        raise


def load_csv(db, csv_path=CSV_PATH):
    # Scalability:each CSV has its own collection
    collection_name = Path(csv_path).stem
    col = db[collection_name]

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"{csv_path} not found.")

    df = pd.read_csv(csv_path)
    df["Discount"] = df["Discount"].str.replace("%", "").astype(float)
    df["LaunchDate"] = pd.to_datetime(df["LaunchDate"], dayfirst=True)

    col.delete_many({})
    col.insert_many(df.to_dict("records"))
    log.info("Loaded %d rows into collection '%s'", len(df), collection_name)

    # Efficiency:indexes for fast queries
    col.create_index([("Price",    ASCENDING)])
    col.create_index([("Rating",   ASCENDING)])
    col.create_index(
        [("Category", ASCENDING), ("Rating", ASCENDING)])  # compound
    log.info("Indexes created.")

    return col, df
# Runing MongoDB Query


def run_query(col, query):
    def fix_dates(obj):
        if isinstance(obj, dict):
            if "$date" in obj:
                return datetime.fromisoformat(obj["$date"])
            return {k: fix_dates(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [fix_dates(i) for i in obj]
        return obj

    try:
        cursor = col.find(fix_dates(query.get("filter", {})), {"_id": 0})
        if query.get("sort"):
            cursor = cursor.sort(query["sort"])
        results = list(cursor)
        log.info("Query returned %d result(s)", len(results))
        return results
    except Exception as e:
        log.error("Query execution failed: %s", e)
        return []
