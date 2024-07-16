#!/usr/bin/env python3
"""8-all.py"""


from pymongo.collection import Collection
from typing import List


def list_all(mongo_collection: Collection) -> List[dict]:
    """Lists all documents in a MongoDB collection.

    Args:
        mongo_collection: A pymongo collection object.

    Return:
        A list of dictionaries.
    """
    documents = mongo_collection.find()
    return list(documents)
