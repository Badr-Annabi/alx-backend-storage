#!/usr/bin/env python3
"""
This Python function changes all topics of a school document based on the name
"""


def update_topics(mongo_collection, name, topics):
    """Updates Documents"""
    new_document = mongo_collection.update(
            {"name": name},
            {
                "set": {"topics": topics}
            })
