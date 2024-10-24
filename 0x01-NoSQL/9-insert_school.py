#!/usr/bin/env python3
"""
    Inserts a new document into a MongoDB collection.
"""

def insert_school(mongo_collection, **kwargs):
    """
    Args:
    mongo_collection: The pymongo collection object.
    **kwargs: Key-value pairs representing the document fields and their values.

    Returns:
    The inserted document's ID.
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
