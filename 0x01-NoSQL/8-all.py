#!/usr/bin/env python3
""" 8. List all documents in Python
"""

def list_all(mongo_collection):
    """
    Lists all documents in a MongoDB collection.
    
    Args:
    mongo_collection: The pymongo collection object.

    Returns:
    list: A list of documents in the collection or an empty list if no documents exist.
    """
    return list(mongo_collection.find())
