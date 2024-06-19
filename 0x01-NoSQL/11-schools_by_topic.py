#!/usr/bin/env python3

"""Returns the list of school having a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns a list of schools with a specific topic.

    Args:
        mongo_collection (pymongo.collection.Collection): A pymongo collection
        object.
        topic (str): The topic to search for.

    Returns:
        list: A list of dictionaries representing the matching schools.
    """
    return list(mongo_collection.find({"topics": topic}))
