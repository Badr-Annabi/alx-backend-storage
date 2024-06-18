#!/usr/bin/env python3
"""
This Python function returns the list of school having a specific topic
"""


def schools_by_topics(mongo_collection, topic):
    """ returns list of specific topic"""
    return mongo_collection.find({"topics": topic})
