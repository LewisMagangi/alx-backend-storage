#!/usr/bin/env python3
"""
Changes all topics of a school document based on the name.
"""

def update_topics(mongo_collection, name, topics):
    """
    Updates the topics for the specified school name.

    Args:
    mongo_collection: The pymongo collection object.
    name (str): The school name to update.
    topics (list): A list of topics to set for the school.

    Returns:
    None
    """
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )

