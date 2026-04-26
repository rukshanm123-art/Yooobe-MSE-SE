import sqlite3
import hashlib
from datetime import datetime
from abc import ABC, abstractmethod


# ==========================================
# 1. DATABASE & SINGLETON PATTERN
# ==========================================

class DatabaseManager:
    """
    Singleton class to handle SQLite database connections and schema.
    Ensures only one connection instance exists.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            # Initialize database connection and tables
            cls._instance.conn = sqlite3.connect('car_rental.db')
            cls._instance.cursor = cls._instance.conn.cursor()
            cls._instance.create_tables()
        return cls._instance

    def create_tables(self):
        # Users Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password_hash TEXT,
                role TEXT
            )
        ''')
        # Cars Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                make TEXT,
                model TEXT,
                year INTEGER,
                mileage INTEGER,
                available INTEGER DEFAULT 1, -- 1=True, 0=False
                min_rent_period INTEGER,
                max_rent_period INTEGER,
                daily_rate REAL
            )
        ''')
        # Bookings Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                car_id INTEGER,
                start_date TEXT,
                end_date TEXT,
                total_fee REAL,
                status TEXT DEFAULT 'PENDING',
                FOREIGN KEY(customer_id) REFERENCES users(id),
                FOREIGN KEY(car_id) REFERENCES cars(id)
            )
        ''')
        self.conn.commit()

        # Seed an admin if none exists for easy testing
        self.cursor.execute("SELECT * FROM users WHERE role='ADMIN'")
        if not self.cursor.fetchone():
            # Default Admin: username 'admin', password 'admin123'
            pw_hash = hashlib.sha256("admin123".encode()).hexdigest()
            self.cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                                ('admin', pw_hash, 'ADMIN'))
            self.conn.commit()


# ==========================================
# 2. USER HIERARCHY & FACTORY PATTERN
# ==========================================

class User(ABC):
    """Abstract Base Class for all users."""

    def __init__(self, user_id, username, role):
        self.user_id = user_id
        self.username = username
        self.role = role


class Admin(User):
    """Admin user with privileges for car and booking management."""

    def __init__(self, user_id, username):
        super().__init__(user_id, username, "ADMIN")


class Customer(User):
    """Customer user with privileges for viewing and booking cars."""

    def __init__(self, user_id, username):
        super().__init__(user_id, username, "CUSTOMER")


class UserFactory:
    """Factory Pattern to create User objects based on role."""

    @staticmethod
    def create_user(user_id, username, role):
        if role == 'ADMIN':
            return Admin(user_id, username)
        elif role == 'CUSTOMER':
            return Customer(user_id, username)
        else:
            raise ValueError("Invalid Role")


# ==========================================
# 3. RENTAL SYSTEM (SERVICE/BUSINESS LOGIC)
# ==========================================

class RentalSystem:
    def __init__(self):
        self.db = DatabaseManager()
        self.current_user = None

    # --- Authentication (Requirement a) ---
    def register(self, username, password, role='CUSTOMER'):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.db.cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                                   (username, password_hash, role))
            self.db.conn.commit()
            print("Registration successful!")
        except sqlite3.IntegrityError:
            print("Username already exists.")

    def login(self, username, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.db.cursor.execute("SELECT id, username, role FROM users WHERE username=? AND password_hash=?",
                               (username, password_hash))
        row = self.db.cursor.fetchone()
        if row:
            self.current_user = UserFactory.create_user(row[0], row[1], row[2])
            print(f"Welcome, {self.current_user.username} ({self.current_user.role})")
            return True
        else:
            print("Invalid credentials.")
            return False

    def logout(self):
        self.current_user = None

    # --- Car Management (Requirement d) ---
    def add_car(self, make, model, year, mileage, min_period, max_period, rate):
        if not isinstance(self.current_user, Admin):
            print("Access Denied: Admins only.")
            return

        self.db.cursor.execute('''
            INSERT INTO cars (make, model, year, mileage, min_rent_period, max_rent_period, daily_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (make, model, year, mileage, min_period, max_period, rate))
        self.db.conn.commit()
        print(f"Car {make} {model} added successfully.")

    def view_cars(self, show_all=False):
        # Requirement e: View available cars
        query = "SELECT * FROM cars"
        if not show_all:
            query += " WHERE available=1"

        self.db.cursor.execute(query)
        cars = self.db.cursor.fetchall()

        print(f"\n{'ID':<5} {'Make':<10} {'Model':<10} {'Year':<6} {'Rate/Day':<10} {'Available'}")
        print("-" * 60)
        if not cars:
            print("No cars in the inventory.")
            return

        for car in cars:
            # car tuple: (id, make, model, year, mileage, avail, min, max, rate)
            avail_status = "Yes" if car[5] else "No"
            print(f"{car[0]:<5} {car[1]:<10} {car[2]:<10} {car[3]:<6} ${car[8]:<9} {avail_status}")

    # --- Booking Logic (Requirement f, g) ---
    def book_car(self, car_id, start_str, end_str):
        if not isinstance(self.current_user, Customer):
            print("Only customers can book cars.")
            return

        try:
            start_date = datetime.strptime(start_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_str, "%Y-%m-%d")

            # Fetch car details
            self.db.cursor.execute("SELECT * FROM cars WHERE id=?", (car_id,))
            car = self.db.cursor.fetchone()

            if not car:
                print("Car not found.")
                return
            if car[5] == 0:
                print("Car is not available.")
                return

            # Logic: Validate Dates
            days = (end_date - start_date).days
            if days <= 0:
                print("End date must be after start date.")
                return

            # Constraint Checks (Requirement c details)
            min_p, max_p, rate = car[6], car[7], car[8]
            if days < min_p:
                print(f"Booking rejected: Minimum rental period is {min_p} days.")
                return
            if days > max_p:
                print(f"Booking rejected: Maximum rental period is {max_p} days.")
                return

            # Requirement g: Calculate Fee
            total_fee = days * rate

            # Create Booking
            self.db.cursor.execute('''
                INSERT INTO bookings (customer_id, car_id, start_date, end_date, total_fee, status)
                VALUES (?, ?, ?, ?, ?, 'PENDING')
            ''', (self.current_user.user_id, car_id, start_str, end_str, total_fee))
            self.db.conn.commit()
            print(f"Booking request sent! Total estimated fee: ${total_fee:.2f}")
            print("Status: PENDING (Waiting for Admin approval)")

        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")

    # --- New Feature: View Customer History ---
    def view_booking_history(self):
        # Security check: Ensure only customers can access this
        if not isinstance(self.current_user, Customer):
            print("Only customers can view booking history.")
            return

        # Query to join Bookings with Cars to get readable details
        query = '''
            SELECT b.id, c.make, c.model, b.start_date, b.end_date, b.total_fee, b.status
            FROM bookings b
            JOIN cars c ON b.car_id = c.id
            WHERE b.customer_id = ?
            ORDER BY b.id DESC
        '''
        self.db.cursor.execute(query, (self.current_user.user_id,))
        bookings = self.db.cursor.fetchall()

        if not bookings:
            print("\nYou have no booking history.")
            return

        print(f"\n--- Your Booking History ---")
        print(f"{'ID':<5} {'Car':<20} {'Dates':<25} {'Total':<10} {'Status'}")
        print("-" * 75)

        for b in bookings:
            # b structure: (id, make, model, start, end, fee, status)
            car_name = f"{b[1]} {b[2]}"
            date_range = f"{b[3]} to {b[4]}"
            status = b[6]

            print(f"{b[0]:<5} {car_name:<20} {date_range:<25} ${b[5]:<9.2f} {status}")

    # --- Rental Management (Requirement h) ---
    def manage_bookings(self):
        if not isinstance(self.current_user, Admin):
            print("Access Denied: Admins only.")
            return

        self.db.cursor.execute('''
            SELECT b.id, u.username, c.make, c.model, b.start_date, b.end_date, b.total_fee, b.status, b.car_id
            FROM bookings b
            JOIN users u ON b.customer_id = u.id
            JOIN cars c ON b.car_id = c.id
            WHERE b.status = 'PENDING'
        ''')
        bookings = self.db.cursor.fetchall()

        if not bookings:
            print("No pending bookings.")
            return

        print("\n--- Pending Bookings ---")
        for b in bookings:
            print(f"ID: {b[0]} | User: {b[1]} | Car: {b[2]} {b[3]} | Fee: ${b[6]} | Dates: {b[4]} to {b[5]}")

        b_id = input("Enter Booking ID to process (or 'q' to quit): ")
        if b_id == 'q': return

        try:
            # Find the full booking record to get car_id
            booking_to_process = next((b for b in bookings if str(b[0]) == b_id), None)
            if not booking_to_process:
                print("Invalid Booking ID.")
                return

            car_id = booking_to_process[8]

            action = input("Approve (a) or Reject (r)? ").lower()

            if action == 'a':
                self.db.cursor.execute("UPDATE bookings SET status='APPROVED' WHERE id=?", (b_id,))
                # Lock the car (Availability = 0)
                self.db.cursor.execute("UPDATE cars SET available=0 WHERE id=?", (car_id,))
                self.db.conn.commit()
                print("Booking Approved. Car availability updated.")
            elif action == 'r':
                self.db.cursor.execute("UPDATE bookings SET status='REJECTED' WHERE id=?", (b_id,))
                # Car remains available, no need to update cars table
                self.db.conn.commit()
                print("Booking Rejected.")
            else:
                print("Invalid action.")
        except Exception as e:
            print(f"An error occurred: {e}")


# ==========================================
# 4. MAIN INTERFACE (CLI)
# ==========================================

def main():
    system = RentalSystem()

    while True:
        print("\n=== CAR RENTAL SYSTEM ===")
        if not system.current_user:
            # Not Logged In Menu
            print("1. Login")
            print("2. Register")
            print("3. Exit")
            choice = input("Select: ")

            if choice == '1':
                u = input("Username: ")
                p = input("Password: ")
                system.login(u, p)
            elif choice == '2':
                u = input("Username: ")
                p = input("Password: ")
                # Simple role assignment for demo purposes
                role = 'CUSTOMER'
                system.register(u, p, role)
            elif choice == '3':
                break

        else:
            # Logged In Menu
            print(f"\nLogged in as: {system.current_user.username}")
            print("1. View Available Cars")

            if isinstance(system.current_user, Admin):
                print("2. Add New Car")
                print("3. Manage Bookings")
            elif isinstance(system.current_user, Customer):
                print("2. Book a Car")
                print("3. View Booking History")  # <-- Customer history

            print("4. Logout")
            choice = input("Select: ")

            if choice == '1':
                system.view_cars(show_all=isinstance(system.current_user, Admin))

            elif choice == '2':
                if isinstance(system.current_user, Admin):
                    # Admin: Add Car Logic
                    try:
                        make = input("Make: ")
                        model = input("Model: ")
                        year = int(input("Year: "))
                        mileage = int(input("Mileage: "))
                        min_p = int(input("Min Rent Days: "))
                        max_p = int(input("Max Rent Days: "))
                        rate = float(input("Daily Rate: "))
                        system.add_car(make, model, year, mileage, min_p, max_p, rate)
                    except ValueError:
                        print("Invalid input for year, mileage, periods, or rate. Please use numbers.")
                else:
                    # Customer: Book Car Logic
                    c_id = input("Enter Car ID: ")
                    start = input("Start Date (YYYY-MM-DD): ")
                    end = input("End Date (YYYY-MM-DD): ")
                    system.book_car(c_id, start, end)

            # Handle Option 3 for Admin vs Customer
            elif choice == '3':
                if isinstance(system.current_user, Admin):
                    system.manage_bookings()
                elif isinstance(system.current_user, Customer):
                    system.view_booking_history()  # <-- Call the new function

            elif choice == '4':
                system.logout()


if __name__ == "__main__":
    main()