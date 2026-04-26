import logging
import os
import sqlite3


class RentalSystem:
    """
    Design Pattern: Singleton
    Ensures only one instance of the rental system exists,
    centralizing data management for users, cars, and bookings.
    """
    _instance = None


    DB_PATH = "database/rental.db"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RentalSystem, cls).__new__(cls)
            cls._instance.users = {}
            cls._instance.cars = []
            cls._instance.bookings = []

            #Professional Logging setup
            if not os.path.exists("logs"):
                os.makedirs("logs")
            logging.basicConfig(
                filename="logs/system.log",
                level=logging.INFO,
                format="%(asctime)s - %(message)s"
            )

            #Minimal Restore: Load users/cars from SQLite (does not change booking logic)
            cls._instance._load_users_from_db()
            cls._instance._load_cars_from_db()

        return cls._instance


    #SQLITE LOADING (MINIMAL PERSISTENCE RESTORE)


    def _load_users_from_db(self):
        """
        Loads users from SQLite into in-memory dictionary.
        Keeps the system behavior unchanged; it only restores saved state.
        If DB/table doesn't exist, it safely skips loading.
        """
        try:
            if not os.path.exists(self.DB_PATH):
                logging.info("SQLite DB not found. Skipping user load.")
                return

            conn = sqlite3.connect(self.DB_PATH)
            cur = conn.cursor()

            #Expected schema: users(username TEXT, password TEXT, role TEXT)
            cur.execute("SELECT username, password, role FROM users")
            rows = cur.fetchall()

            from .models import Admin, Customer

            for username, password, role in rows:
                #Defensive handling for unexpected role values
                if role == "Admin":
                    self.users[username] = Admin(username, password)
                elif role == "Customer":
                    self.users[username] = Customer(username, password)

            conn.close()
            logging.info(f"Loaded {len(rows)} users from SQLite.")

        except Exception as e:
            logging.warning(f"User load skipped: {e}")

    def _load_cars_from_db(self):
        """
        Loads cars from SQLite into in-memory list.
        If DB/table doesn't exist, it safely skips loading.
        """
        try:
            if not os.path.exists(self.DB_PATH):
                logging.info("SQLite DB not found. Skipping car load.")
                return

            conn = sqlite3.connect(self.DB_PATH)
            cur = conn.cursor()

            #Expected schema fields:
            #cars(car_id INT, make TEXT, model TEXT, year INT, mileage INT,
            #daily_rate INT, min_days INT, max_days INT, is_available INT)
            cur.execute("""
                SELECT car_id, make, model, year, mileage, daily_rate, min_days, max_days, is_available
                FROM cars
            """)
            rows = cur.fetchall()

            from .models import Car

            for r in rows:
                car = Car(
                    c_id=r[0],
                    make=r[1],
                    model=r[2],
                    year=r[3],
                    mileage=r[4],
                    rate=r[5],
                    min_d=r[6],
                    max_d=r[7]
                )
                car.is_available = bool(r[8])
                self.cars.append(car)

            conn.close()
            logging.info(f"Loaded {len(rows)} cars from SQLite.")

        except Exception as e:
            logging.warning(f"Car load skipped: {e}")


    #VERSION 2 (INNOVATION): SMART BOOKING INTELLIGENCE FUNCTIONS


    def calculate_discount_rate(self, days: int) -> float:
        """
        Dynamic discount rules:
        - >= 14 days => 10% discount
        - >= 7 days  => 5% discount
        Validations:
        - days must be a positive integer
        """
        if not isinstance(days, int) or days <= 0:
            return 0.0

        if days >= 14:
            return 0.10
        if days >= 7:
            return 0.05
        return 0.0

    def pricing_breakdown(self, daily_rate: int, days: int) -> dict:
        """
        Explainable pricing breakdown:
        Provides transparent calculation including discount.
        Validations:
        - daily_rate must be >= 0
        - days must be > 0
        """
        if not isinstance(daily_rate, int) or daily_rate < 0:
            daily_rate = 0
        if not isinstance(days, int) or days <= 0:
            days = 1

        base = daily_rate * days
        disc_rate = self.calculate_discount_rate(days)
        disc_amount = int(base * disc_rate)
        final = max(0, base - disc_amount)

        return {
            "daily_rate": daily_rate,
            "days": days,
            "base": base,
            "discount_rate": disc_rate,
            "discount_amount": disc_amount,
            "final_total": final
        }

    def recommend_cars(self, target_rate: int, limit: int = 3):
        """
        Smart Rental Recommendations:
        Recommends available cars closest in price to the target_rate.
        Validations:
        - target_rate must be >= 0
        - limit must be 1..10
        """
        if not isinstance(target_rate, int) or target_rate < 0:
            target_rate = 0
        if not isinstance(limit, int):
            limit = 3
        limit = max(1, min(limit, 10))

        available = [c for c in self.cars if getattr(c, "is_available", False)]
        if not available:
            return []

        available.sort(key=lambda c: abs(getattr(c, "daily_rate", 0) - target_rate))
        return available[:limit]

    def get_user_risk_score(self, username: str) -> int:
        """
        Customer Risk Score:
        - Rejected booking: +20
        - Pending booking:  +10
        - Approved booking: +0
        Validations:
        - username must be a non-empty string
        """
        if not isinstance(username, str) or not username.strip():
            return 0

        score = 0
        for b in self.bookings:
            if getattr(b, "user", None) == username:
                status = getattr(b, "status", "")
                if status == "Rejected":
                    score += 20
                elif status == "Pending":
                    score += 10
        return score

    def risk_level(self, score: int) -> str:
        """
        Converts a numeric score into LOW / MEDIUM / HIGH.
        """
        if not isinstance(score, int) or score < 0:
            score = 0

        if score >= 50:
            return "HIGH"
        if score >= 20:
            return "MEDIUM"
        return "LOW"


    #ADMIN FEATURES: CAR MANAGEMENT (CRUD)


    def add_car(self, make, model, year, mil, rate, min_r, max_r):
        """
        Adds a new car to the Vehicles with validation.
        """
        from .models import Car

        #Validation: ensure meaningful values
        if not make or not model:
            return "!!! Error: Make and model cannot be empty."
        if year <= 0 or mil < 0 or rate < 0:
            return "!!! Error: Year, mileage, and rate must be valid positive numbers."
        if min_r <= 0 or max_r <= 0 or min_r > max_r:
            return "!!! Error: Min days must be <= Max days, and both must be > 0."

        c_id = len(self.cars) + 1
        new_car = Car(c_id, make, model, year, mil, rate, min_r, max_r)
        self.cars.append(new_car)

        logging.info(f"Admin added car: {make} {model} (ID: {c_id})")
        return f"Successfully added {make} {model} (ID: {c_id})."

    def update_car_mileage(self, car_id, new_mileage):
        """
        Updates car mileage safely.
        """
        if car_id <= 0 or new_mileage < 0:
            return False

        for car in self.cars:
            if car.car_id == car_id:
                old_mil = car.mileage
                car.mileage = new_mileage
                logging.info(f"Admin updated Car {car_id} mileage: {old_mil} -> {new_mileage}")
                return True
        return False

    def remove_car(self, car_id):
        """
        Removes a car from Vehicles..
        """
        if car_id <= 0:
            return False

        initial_count = len(self.cars)
        self.cars = [c for c in self.cars if c.car_id != car_id]
        if len(self.cars) < initial_count:
            logging.info(f"Admin removed car ID: {car_id}")
            return True
        return False


    #CUSTOMER FEATURES

    def book_car(self, user, car_id, days):
        """
        Booking Logic:
        - Validates availability
        - Validates rental period
        - Uses Version 2 pricing breakdown (discount + explainable output)
        """
        #Basic validations
        if car_id <= 0:
            return "!!! Error: Invalid car ID."
        if not isinstance(days, int) or days <= 0:
            return "!!! Error: Days must be a positive integer."

        car = next((c for c in self.cars if c.car_id == car_id and c.is_available), None)
        if not car:
            return "!!! Error: Car is unavailable or ID is invalid."

        #Validate rental period (existing requirement)
        if not (car.min_days <= days <= car.max_days):
            return f"!!! Error: Rental must be between {car.min_days} and {car.max_days} days."

        #Version 2 pricing breakdown + discount
        breakdown = self.pricing_breakdown(car.daily_rate, days)
        total = breakdown["final_total"]

        from .models import Booking
        b_id = len(self.bookings) + 1
        new_b = Booking(b_id, user.get_username(), car, days, total)
        self.bookings.append(new_b)

        logging.info(f"Booking Request: {user.get_username()} for Car {car_id}")

        return (
            f"Success! Booking #{b_id} is Pending.\n"
            f"Base: {breakdown['days']} days × ${breakdown['daily_rate']}/day = ${breakdown['base']}\n"
            f"Discount: {int(breakdown['discount_rate'] * 100)}% (-${breakdown['discount_amount']})\n"
            f"Final Total: ${breakdown['final_total']}."
        )


    #ADMIN FEATURES: BOOKING MANAGEMENT


    def update_booking_status(self, b_id, status):
        """
        Admin approves/rejects a booking.
        When approved: updates car availability to False.
        """
        if b_id <= 0:
            return False
        if status not in ["Approved", "Rejected"]:
            return False

        for b in self.bookings:
            if b.b_id == b_id:
                b.status = status

                #If approved, update car availability
                if status == "Approved":
                    for car in self.cars:
                        if f"{car.make} {car.model}" == b.car_info:
                            car.is_available = False

                logging.info(f"Booking {b_id} status updated to: {status}")
                return True
        return False
