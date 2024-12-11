import pymongo
from pymongo.results import InsertManyResult
from typing import Optional

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["songs"]

def create_genre_collection(genre: str, track_data: list[dict]) -> (InsertManyResult, Optional[str]):
    try:
        genre_col = db[genre]
        docs = genre_col.insert_many(track_data)
        return docs, None

    except Exception as error:
        return None, str(error)

def clear_database():
    collection_names = db.list_collection_names()
    for name in collection_names:
        db[name].drop()
