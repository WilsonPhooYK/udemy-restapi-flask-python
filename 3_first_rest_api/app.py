from __future__ import annotations
from flask import Flask, jsonify, request, render_template
from typing import TypedDict, cast

import flask

# __name__ gives each file a unique name
app = Flask(__name__)

# @app.route('/') # 'http://www.google.com/'
# def home():
#     return "Hello world!"

# POST - used to receive data
# GET - used to send data back only
StoreItemType = TypedDict(
    "StoreItemType",
    {
        "name": str,
        "price": float,
    },
)

StoreType = TypedDict(
    "StoreType",
    {
        "name": str,
        "items": list[StoreItemType],
    },
)
PostStoreType = TypedDict("PostStoreType", {"name": str})
JSONResponseType = flask.wrappers.Response

stores: list[StoreType] = [
    {
        "name": "My Wonderful Store",
        "items": [
            {
                "name": "My Item",
                "price": 15.99,
            }
        ],
    }
]


@app.route("/")
def home() -> str:
    return render_template("index.html")


# POST /store data: {name:}
@app.route("/store", methods=["POST"])
def create_store() -> JSONResponseType:
    try:
        request_data: PostStoreType = cast(PostStoreType, request.get_json())
        if not request_data.get("name"):
            raise ValueError(f"'name' required, type={type(request_data)}")

        store_result: StoreType | None = next(
            (
                store
                for store in stores
                if store["name"].lower().replace(" ", "_") == request_data["name"]
            ),
            None,
        )
        if store_result:
            raise LookupError(f"Duplicated store: {request_data['name']}")

        new_store: StoreType = {"name": request_data["name"], "items": []}
        stores.append(new_store)
        stores_json: JSONResponseType = jsonify(stores)
        return stores_json
    except ValueError as e:
        return flask.make_response({"error_message": str(e)}, 400)
    except LookupError as e:
        return flask.make_response({"error_message": str(e)}, 400)


# GET /store/<string:name>
@app.route("/store/<string:name>")
def get_store(name: str) -> JSONResponseType:
    try:
        store_result: StoreType = next(
            store for store in stores if store["name"].lower().replace(" ", "_") == name
        )
        store_json: JSONResponseType = jsonify(store_result)
        return store_json
    except StopIteration:
        return flask.make_response({"error_message": "Store not found"}, 400)


# GET /store
@app.route("/store")
def get_stores() -> JSONResponseType:
    stores_json: JSONResponseType = jsonify(stores)
    return stores_json


# POST /store/<string:name>/item {name:, price:}
@app.route("/store/<string:name>/item", methods=["POST"])
def create_item_in_store(name: str) -> JSONResponseType:
    try:
        # type: ignore
        request_data: StoreItemType = cast(StoreItemType, request.get_json())
        if not request_data:
            raise ValueError("Invalid request")
        if not (request_data.get("name") and request_data.get("price") != None):
            raise ValueError(f"'name', 'price' required, type={type(request_data)}")

        store_result: StoreType = next(
            store for store in stores if store["name"].lower().replace(" ", "_") == name
        )

        item_result: StoreItemType | None = next(
            (
                item
                for item in store_result["items"]
                if item["name"].lower().replace(" ", "_") == request_data["name"]
            ),
            None,
        )
        if item_result:
            raise LookupError(f"Duplicated item in store: {request_data['name']}")

        store_result["items"].append(request_data)
        items_json: JSONResponseType = jsonify(store_result["items"])
        return items_json
    except ValueError as e:
        return flask.make_response({"error_message": str(e)}, 400)
    except StopIteration:
        return flask.make_response({"error_message": "Store not found"}, 400)
    except LookupError as e:
        return flask.make_response({"error_message": str(e)}, 400)


# GET /store/<string:name>/item
@app.route("/store/<string:name>/item")
def get_item_in_store(name: str) -> JSONResponseType:
    try:
        store_result: StoreType = next(
            store for store in stores if store["name"].lower().replace(" ", "_") == name
        )
        items_json: JSONResponseType = jsonify(store_result["items"])
        return items_json
    except StopIteration:
        return flask.make_response({"error_message": "Store not found"}, 400)


app.run(port=5000)
