from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from typing import TypedDict, Union, cast

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "jose"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

JSONResponseType = tuple[dict[str, str], int]
StoreItemType = TypedDict(
    "StoreItemType",
    {
        "name": str,
        "price": float,
    },
)

items: list[StoreItemType] = []

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
        # try:
        # item: Union[StoreItemType, None] = next(
        #     item for item in items if name == item["name"].lower().replace(" ", "_")
        # )
        # Next will move the iterator in the list
        item: Union[StoreItemType, None] = next(
            filter(lambda item: item["name"].lower().replace(" ", "_") == name, items),
            None,
        )
        return item if item else ({"error_message": "Item not found"}, 404)

    # except StopIteration:
    # return {"error_message": "Item not found"}, 404

    def post(self, name: str) -> Union[tuple[StoreItemType, int], JSONResponseType]:
        if next(
            filter(lambda item: item["name"].lower().replace(" ", "_") == name, items),
            None,
        ):
            return {"message": f"An item with name '{name}' already exists."}, 400

        # Only parse for price
        data: dict[str, float] = Item.parser.parse_args()
        item: StoreItemType = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201

    @jwt_required()
    def delete(self, name: str):
        # Use other block
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message": "Item deleted"}

    def put(self, name: str):
        # Only parse for price
        data: dict[str, float] = Item.parser.parse_args()
    
        item: Union[StoreItemType, None] = next(
            filter(lambda item: item["name"].lower().replace(" ", "_") == name, items),
            None,
        )
        if item is None:
            new_item: StoreItemType = {"name": name, "price": data["price"]}
            items.append(new_item)
        else:
            # Update the whole item
            item.update(cast(StoreItemType, data))

        return item


class ItemList(Resource):
    def get(self) -> list[StoreItemType]:
        return items


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")

app.run(port=5000, debug=True)
