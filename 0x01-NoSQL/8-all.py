#!/usr/bin/env python3
'''
8. List all documents in Python
'''


def list_all(mongo_collection):
    '''
    List all documents in Python
    '''
    if not mongo_collection:
        return []
    return list(mongo_collection.find())
