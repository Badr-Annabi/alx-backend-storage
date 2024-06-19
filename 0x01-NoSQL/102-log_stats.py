#!/usr/bin/env python3
"""This python script provides some stats about Nginx logs stored in MongoDB"""

from pymongo import MongoClient


def log_stats():
    """log stats func"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx
    total = logs_collection.count_documents({})
    
    methods_count = {
            "GET": 0,
            "POST": 0,
            "PUT": 0,
            "PATCH": 0,
            "DELETE": 0
            }
    for method in methods_count:
        methods_count[method] = logs_collection.count_documents({"method": method})

    path = logs_collection.count_documents(
            {"method": "GET", "path": "/status"})
    ips = logs_collection.aggregate([{"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
        ])

    print(f"{total} logs")
    print("Methods:")
    for method, count in methods_count.items():
        print(f"\tmethod {method}: {count}")
    print(f"{path} status check")
    print("IPs:")
    for ip in ips:
        if i == 10:
            break
        print(f"\t{ip.get('_id')}: {ip.get('count')}")
        i += 1


if __name__ == "__main__":
    log_stats()
