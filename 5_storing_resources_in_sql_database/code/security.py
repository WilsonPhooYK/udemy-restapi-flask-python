from werkzeug.security import safe_str_cmp
from user import User

def authenticate(username: str, password: str):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload: dict[str, int]):
    id = payload["identity"]
    return  User.find_by_id(id)