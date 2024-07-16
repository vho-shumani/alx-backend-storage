#!/usr/bin/env python3
"""8-all.py"""
from typing import List, Dict

def list_all(mongo_collection: Collection) -> List[Dict]:
    """"""
    documents = mongo_collection.find()
    return list(documents)
