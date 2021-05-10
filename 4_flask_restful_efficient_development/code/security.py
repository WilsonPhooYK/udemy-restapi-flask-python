from werkzeug.security import safe_str_cmp
from user import User

users: list[User] = [User(1, "bob", "asdf")]
username_mapping: dict[str, User] = {user.username: user for user in users}
userid_mapping: dict[int, User] = {user.id: user for user in users}


def authenticate(username: str, password: str):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload: dict[str, int]):
    user_id = payload["identity"]
    return userid_mapping.get(user_id, None)
