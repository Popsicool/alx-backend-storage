#!/usr/bin/env python3
'''
12. Log stats
'''


from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient()
    collection = client.logs.nginx
    docs = collection.count_documents({})
    print("{} logs".format(docs))
    print("Methods:")
    meths = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for meth in meths:
        meth_cnt = collection.count_documents({"method": meth})
        print("\tmethod {}: {}".format(meth, meth_cnt))
    state = collection.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(state))
