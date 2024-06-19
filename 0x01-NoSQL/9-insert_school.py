#!/usr/bin/env python3

"""Inserts a new document in a collection based on kwargs"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on kwargs

    Args:
        mongo_collection: The collection to insert the document in
        kwargs: The document to insert

    Returns:
        The result of the insert (new _id)
    """
    return mongo_collection.insert(kwargs)
