#!/usr/bin/env python3

"""Provides some stats about Nginx logs stored in MongoDB"""

from pymongo import MongoClient


def analyze_logs(nginx_collection):
    """
    Analyzes Nginx logs stored in a MongoDB collection and displays statistics.

    Args:
        nginx_collection (pymongo.collection.Collection): The MongoDB
        collection containing logs.
    """

    # Count total logs
    total_logs = nginx_collection.count_documents({})

    # Count documents by method (GET, POST, PUT, PATCH, DELETE)
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {}
    for method in methods:
        method_counts[method] = nginx_collection.count_documents(
            {"method": method}
        )

    # Count documents with method=GET and path=/status
    status_checks = nginx_collection.count_documents(
            {"method": "GET", "path": "/status"}
        )

    # Print statistics
    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"\tmethod {method}: {count}")
    print(f"{status_checks} status check")


if __name__ == "__main__":
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017")
    collection = client.logs.nginx

    analyze_logs(collection)

    # Close connection (optional)
    client.close()

if __name__ == "__main__":
    client = MongoClient("mongodb://127.0.0.1:27017")
    db = client.nginx_logs
    print(db.logs.count())
