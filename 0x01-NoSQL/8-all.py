#!/usr/bin/env python3
"""
8-all.py
"""


def list_all(mongo_collection):
    """Lists all documents in a MongoDB collection.

    Args:
        mongo_collection: A pymongo collection object.

    Return:
        A list of dictionaries.
    """
    documents = mongo_collection.find()
    return list(documents)
