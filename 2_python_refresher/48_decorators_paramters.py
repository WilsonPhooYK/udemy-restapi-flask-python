import functools
from typing import Callable

user = { "username": "jose", "access_level": "admin" }

FunctionType = Callable[[], str]

def make_secure(access_level: str):
    def decorator(func: FunctionType) -> FunctionType:
        # Main the original function name
        @functools.wraps(func)
        def secure_function(*args: str, **kwargs: str):
            if user["access_level"] == access_level:
                return func(*args, **kwargs)
            else:
                return f"No {access_level} permissons for {user['username']}."
            
        return secure_function
    
    return decorator


@make_secure("admin")
def get_admin_password() -> str:
    return "1234"

@make_secure("user")
def get_dashboard_password() -> str:
    return "user"

print(get_admin_password())
print(get_dashboard_password())