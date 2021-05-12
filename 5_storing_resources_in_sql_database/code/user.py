import sqlite3
from typing import Any
from flask_restful import Resource, reqparse
from dataclasses import dataclass

JSONResponseType = tuple[dict[str, Any], int]


@dataclass()
class User:
    # Must have id to authenticate
    id: int
    username: str
    password: str

    # def __init__(self, _id: int, username: str, password: str) -> None:
    #     # Must have id to authenticate
    #     self.id = _id
    #     self.username = username
    #     self.password = password

    @classmethod
    def find_by_username(cls, username: str):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        # Parameters have to be tuple
        result = cursor.execute(query, (username,))
        row = result.fetchone()

        global user
        user = None
        if row:
            user = cls(*row)

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id: int):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        # Parameters have to be tuple
        result = cursor.execute(query, (_id,))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username",
        type=str,
        required=True,
        help="This field cannot be left blank!",
    )
    parser.add_argument(
        "password",
        type=str,
        required=True,
        help="This field cannot be left blank!",
    )

    def post(self) -> JSONResponseType:
        data: dict[str, str] = UserRegister.parser.parse_args()
        
        if User.find_by_username(data["username"]):
            return {"error_message": "User exists"}, 400

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"

        cursor.execute(query, (data["username"], data["password"]))
        connection.commit()
        
        connection.close()

        return {"success": True}, 201
