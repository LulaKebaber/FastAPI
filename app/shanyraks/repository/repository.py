from datetime import datetime
from typing import Optional, Any

from bson.objectid import ObjectId
from pymongo.database import Database

from ..utils.security import hash_password


class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, user_id: str, data: dict[str, Any]):
        data["user_id"] = ObjectId("user_id")
        shanyrak = self.database["shanyraks"].insert_one(data)
        return shanyrak.inserted_id
