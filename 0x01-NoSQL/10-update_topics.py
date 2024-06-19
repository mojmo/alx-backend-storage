#!/usr/bin/env python3

"""Changes all topics of a school document based on the name"""


def update_topics(mongo_collection, name, topics):
    """
    Updates the topics of a school document based on the name.

    Args:
        mongo_collection (pymongo.collection.Collection): A pymongo collection
        object.
        name (str): The name of the school document to update.
        topics (list): The list of new topics for the school.

    Returns:
        None
    """

    filter = {"name": name}
    update = {"$set": {"topics": topics}}
    mongo_collection.update_many(filter, update)
