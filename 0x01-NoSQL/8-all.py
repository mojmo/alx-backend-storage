#!/usr/bin/env python3

"""lists all documents in a collection"""


def list_all(mongo_collection):
    """
    Lists all documents in a collection.

    Args:
        mongo_collection (pymongo.collection.Collection): A pymongo collection
        object.

    Returns:
        list: A list of documents from the collection.
    """

    documents = list(mongo_collection.find())
    return documents
