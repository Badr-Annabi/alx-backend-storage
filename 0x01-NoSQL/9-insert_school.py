#!/usr/bin/env python3
"""
This Python function inserts a new document in a collection based on kwargs
"""


def insert_school(mongo_collection, **kwargs):
    """Insert Documents"""
    new_document = mongo_collection.insert_one(kwargs)
    return new_document.inserted_id
