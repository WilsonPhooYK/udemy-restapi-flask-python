import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from typing import Optional, TypedDict, Union

JSONResponseType = tuple[dict[str, str], int]
StoreItemType = TypedDict(
    "StoreItemType",
    {
        "name": str,
        "price": float,
    },
)

# JWT - JSON Web Token

# 400 - bad request
# 404 - item not found
# 201 - create success
# 202 - accepted, but will create success only after a long time
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank!"
    )

    # Authorization - JWT {token}
    @jwt_required()
    def get(self, name: str) -> Union[StoreItemType, JSONResponseType]:
        # Returns the current user row
        print(current_identity)
        item = self.find_by_name(name)
        if item:
            return item

        return {"error_message": "Item not found"}, 404

    # except StopIteration:
    # return {"error_message": "Item not found"}, 404

    @classmethod
    def find_by_name(cls, name: str) -> Optional[StoreItemType]:
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {"name": row[0], "price": row[1]}

    @classmethod
    def insert(cls, item: StoreItemType):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item["name"], item["price"]))

        connection.commit()
        connection.close()

    def post(self, name: str) -> Union[tuple[StoreItemType, int], JSONResponseType]:
        if self.find_by_name(name):
            return {"message": f"An item with name '{name}' already exists."}, 400

        # Only parse for price
        data: dict[str, float] = Item.parser.parse_args()
        item: StoreItemType = {"name": name, "price": data["price"]}

        try:
            self.insert(item)
        except:
            return {
                "error_message": "An error occured inseting the item"
            }, 500  # Internal Server Error

        return item, 201

    @jwt_required()
    def delete(self, name: str) -> JSONResponseType:
        if not self.find_by_name(name):
            return {"message": f"An item with name '{name}' does not exists."}, 400

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name = ?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {"message": "Item deleted"}, 200

    def put(self, name: str) -> Union[tuple[StoreItemType, int], JSONResponseType]:
        # Only parse for price
        data: dict[str, float] = Item.parser.parse_args()
        update_item: StoreItemType = {"name": name, "price": data["price"]}

        if self.find_by_name(name):
            try:
                self.update(update_item)
            except:
                return {
                    "error_message": "An error occured updating the item"
                }, 500  # Internal Server Error
        else:
            try:
                self.insert(update_item)
            except:
                return {
                    "error_message": "An error occured inserting the item"
                }, 500  # Internal Server Error

        return update_item, 200

    @classmethod
    def update(cls, item: StoreItemType):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name =?"
        cursor.execute(query, (item["price"], item["name"]))

        connection.commit()
        connection.close()


class ItemList(Resource):
    def get(self) -> tuple[list[StoreItemType], int]:
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        rows = cursor.execute(query)
        items_list: list[StoreItemType] = [
            {"name": name, "price": price} for name, price in rows.fetchall()
        ]

        connection.close()

        return items_list, 200
