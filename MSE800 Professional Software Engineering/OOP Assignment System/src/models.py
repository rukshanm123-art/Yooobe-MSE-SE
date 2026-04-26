import abc


class User(abc.ABC):
    """
    Abstract base class for system users.
    Enforces a consistent interface through display_menu().
    """
    def __init__(self, username: str, password: str, role: str):
        self._username = username
        self._password = password
        self.role = role

    @abc.abstractmethod
    def display_menu(self):
        pass

    def check_password(self, pw: str) -> bool:
        return self._password == pw

    def get_username(self) -> str:
        return self._username


class Customer(User):
    def __init__(self, username: str, password: str):
        super().__init__(username, password, "Customer")

    def display_menu(self):
        print(f"\n--- CUSTOMER MENU ({self._username}) ---")
        print("1. View Available Cars\n2. Book a Car\n3. View My Status\n4. Logout")


class Admin(User):
    def __init__(self, username: str, password: str):
        super().__init__(username, password, "Admin")

    def display_menu(self):
        print(f"\n--- ADMIN MENU ({self._username}) ---")
        print("1. View Vehicles\n2. Add New Car\n3. Update Car\n4. Remove Car\n5. Manage Bookings\n6. Logout")


class Car:
    """
    Car entity representing rental vehicles.
    """
    def __init__(self, c_id: int, make: str, model: str, year: int,
                 mileage: int, rate: int, min_d: int, max_d: int):
        self.car_id = c_id
        self.make, self.model, self.year = make, model, year
        self.mileage, self.daily_rate = mileage, rate
        self.min_days, self.max_days = min_d, max_d
        self.is_available = True


class Booking:
    """
    Booking entity representing customer rental requests.
    """
    def __init__(self, b_id: int, user: str, car: Car, days: int, total_fee: int):
        self.b_id = b_id
        self.user = user
        self.car_info = f"{car.make} {car.model}"
        self.days = days
        self.total_fee = total_fee
        self.status = "Pending"
