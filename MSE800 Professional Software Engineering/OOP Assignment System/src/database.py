import sqlite3
import os

class Database:
    """
    SQLite Database Layer
    - Automatically creates the database file and tables
    - Requires NO manual configuration
    """

    def __init__(self, db_name="rental.db"):
        #Get project root directory safely
        base_dir = os.path.dirname(os.path.dirname(__file__))
        db_dir = os.path.join(base_dir, "database")

        #Ensure database folder exists
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        #Create/connect SQLite database
        self.db_path = os.path.join(db_dir, db_name)
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()

    def create_tables(self):
        """Create required tables if they do not already exist"""
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            car_id INTEGER PRIMARY KEY AUTOINCREMENT,
            make TEXT,
            model TEXT,
            year INTEGER,
            mileage INTEGER,
            rate INTEGER,
            min_days INTEGER,
            max_days INTEGER,
            is_available INTEGER
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            car_id INTEGER,
            days INTEGER,
            total_fee INTEGER,
            status TEXT
        )
        """)

        self.conn.commit()
