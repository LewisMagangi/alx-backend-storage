#!/usr/bin/env python3
"""
Returns the list of schools having a specific topic.
"""

def schools_by_topic(mongo_collection, topic):
    """
    Finds all schools with a specific topic.

    Args:
    mongo_collection: The pymongo collection object.
    topic (str): The topic to search for.

    Returns:
    list: A list of schools that have the specified topic.
    """
    return list(mongo_collection.find({"topics": topic}))

