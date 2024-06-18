#!/usr/bin/env python3
"""This Python function that lists all documents in a collection"""


def list_all(mongo_collection):
    """Lists all documents"""
    documents = mongo_collection.find()
    return list(documents) if documents else []
