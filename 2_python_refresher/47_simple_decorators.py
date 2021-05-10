import functools
from typing import Callable, Union

user = { "username": "jose", "access_level": "admin" }

FunctionType = Callable[[Union[str, Union[str, str]]], str]

# def get_admin_password() -> str:
#     return "1234"

def make_secure(func: FunctionType) -> FunctionType:
    # Main the original function name
    @functools.wraps(func)
    def secure_function(*args: str, **kwargs: str):
        if user["access_level"] == "admin":
            return func(*args, **kwargs)
        else:
            return f"No admin permissons for {user['username']}."
        
    return secure_function

# get_admin_password_secure = make_secure(get_admin_password)

@make_secure
def get_admin_password(panel: str) -> str:
    if panel == "admin":
        return "1234"
    elif panel == 'billing':
        return "Super secure password"
    
    return "None"

print(get_admin_password("billing"))