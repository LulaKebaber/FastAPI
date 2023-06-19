from typing import Any
from datetime import datetime

from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import UpdateResult, DeleteResult

from fastapi import HTTPException


class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, user_id: str, data: dict[str, Any]):
        data["user_id"] = ObjectId(user_id)
        insert_result = self.database["shanyraks"].insert_one(data)
        return insert_result.inserted_id

    def get_shanyrak(self, shanyrak_id: str, user_id: str):
        shanyraks = self.database["shanyraks"]
        shanyrak = shanyraks.find_one(
            {"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)}
        )
        return shanyrak
        # hardcode but flake8...

    def update_shanyrak(
        self, shanyrak_id: str, user_id: str, data: dict[str, Any]
    ) -> UpdateResult:
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)},
            update={"$set": data},
        )

    def delete_shanyrak(self, shanyrak_id: str, user_id: str) -> DeleteResult:
        return self.database["shanyraks"].delete_one(
            {"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)}
        )

    def create_comment(self, shanyrak_id: str, user_id: str, input: dict):
        input["shanyrak_id"] = ObjectId(shanyrak_id)
        input["author_id"] = user_id
        input["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        input["user_id"] = ObjectId(user_id)

        shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})

        if not shanyrak:
            raise HTTPException(
                status_code=404, detail=f"Could find shanyrak with id {shanyrak_id}"
            )

        comment = self.database["comments"].insert_one(input)
        return comment.acknowledged

    def get_comments(self, shanyrak_id: str):
        comments = self.database["comments"]
        return list(comments.find({"shanyrak_id": ObjectId(shanyrak_id)}))

    def update_comment(self, comment_id: str, user_id: str, input: str) -> UpdateResult:
        return self.database["comments"].update_one(
            filter={"_id": ObjectId(comment_id), "user_id": ObjectId(user_id)},
            update={"$set": input},
        )

    def delete_comment(self, comment_id: str, user_id) -> DeleteResult:
        return self.database["comments"].delete_one(
            {"_id": ObjectId(comment_id), "user_id": ObjectId(user_id)}
        )
