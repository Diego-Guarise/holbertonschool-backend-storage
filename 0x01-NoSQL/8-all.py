#!/usr/bin/env python3
""" Write a Python function that lists all documents in a collection: """


def list_all(mongo_collection):
    """ Return an empty list if no document in the collection """
    return [tmp for tmp in mongo_collection.find()]
