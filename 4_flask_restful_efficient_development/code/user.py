class User:
    def __init__(self, _id: int, username: str, password: str) -> None:
        # Must have id to authenticate
        self.id = _id
        self.username = username
        self.password = password