from .models import Customer, Admin


class UserFactory:

    #Design Pattern: Factory Method
    #Encapsulates user object creation and role validation.


    @staticmethod
    def create_user(username: str, password: str, role: str, secret: str = ""):
        #Normalize role input
        role_type = role.lower().strip()

        if not username or not password:
            raise ValueError("Username and password cannot be empty.")

        if role_type == "admin":
            if secret == "yoobee":
                return Admin(username, password)
            raise PermissionError("Unauthorized: Invalid Admin Secret Key.")

        if role_type == "customer":
            return Customer(username, password)

        raise ValueError(f"Invalid role: '{role}'. Please use 'admin' or 'customer'.")
