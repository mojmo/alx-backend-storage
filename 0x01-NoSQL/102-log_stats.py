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
        count = nginx_collection.count_documents({"method": method})
        method_counts[method] = count

    # Count documents with method=GET and path=/status
    status_checks = nginx_collection.count_documents(
            {"method": "GET", "path": "/status"}
        )

    # Find top 10 IP addresses by frequency (aggregation)
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},  # Sort by count descending
        {"$limit": 10},  # Limit to top 10 results
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ]
    ip_counts = nginx_collection.aggregate(pipeline)

    # Print statistics
    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"\tmethod {method}: {count}")
    print(f"{status_checks} status check")
    print("IPs:")
    for ip_count in ip_counts:
        ip = ip_count["_id"]
        count = ip_count["count"]
        print(f"\t{ip}: {count}")


if __name__ == "__main__":
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017")
    collection = client.logs.nginx

    analyze_logs(collection)
