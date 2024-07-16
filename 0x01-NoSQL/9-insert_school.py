#!/usr/bin/env python3
"""Module  inserts a new document in a collection based on kwargs"""


def insert_school(mongo_collection, **kwargs):
    """insert anew documents in collection
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
