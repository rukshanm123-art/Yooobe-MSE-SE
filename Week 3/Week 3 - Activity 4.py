"""

PROJECT: College Database Management System (Week 3 - Activity 4)

This project uses Python's Object-Oriented Programming (OOP) to build and manage a basic College Database using the SQLite tool.
I created a "CollegeDB" class that handles everything setting up the tables for Students, Courses, and Teachers,
filling them with sample data, and then running specific queries.
The main goal is to show how we can ask the database questions, specifically, How many students are taking the MSE800 course?
and Which teachers are teaching the MSE801 course?
This project includes inline comments for clarity.

"""


import sqlite3

#Database Class
class CollegeDB:

    def __init__(self, db_name="college.db"):
        #Connect to SQLite database
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    #Clears all tables
    def clear_database(self):
        #Drop all tables to ensure a completely clean start
        self.cursor.execute("DROP TABLE IF EXISTS Student")
        self.cursor.execute("DROP TABLE IF EXISTS Course")
        self.cursor.execute("DROP TABLE IF EXISTS Teacher")
        self.cursor.execute("DROP TABLE IF EXISTS Assign")
        self.cursor.execute("DROP TABLE IF EXISTS Deliver")
        self.conn.commit()
        print("\nDatabase tables cleared successfully!")

    #Create All Tables
    def create_tables(self):
        #STUDENT table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Student(
            Stu_ID INTEGER PRIMARY KEY,
            Stu_FName TEXT,
            Stu_LName TEXT,
            Stu_Add TEXT,
            Stu_Course TEXT
        )
        """)
        #COURSE table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Course(
            C_ID TEXT PRIMARY KEY,
            C_Name TEXT,
            C_Dur INTEGER,
            C_Cred INTEGER
        )
        """)
        #TEACHER table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Teacher(
            T_ID INTEGER PRIMARY KEY,
            T_FName TEXT,
            T_LName TEXT
        )
        """)
        #ASSIGN table (Many-to-Many: Student ↔ Course)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Assign(
            Stu_ID INTEGER,
            C_ID TEXT,
            Assign_Date TEXT,
            FOREIGN KEY (Stu_ID) REFERENCES Student(Stu_ID),
            FOREIGN KEY (C_ID) REFERENCES Course(C_ID)
        )
        """)
        #DELIVER table (Many-to-Many: Teacher ↔ Course)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Deliver(
            T_ID INTEGER,
            C_ID TEXT,
            Deliver_Time TEXT,
            FOREIGN KEY (T_ID) REFERENCES Teacher(T_ID),
            FOREIGN KEY (C_ID) REFERENCES Course(C_ID)
        )
        """)
        self.conn.commit()
        print("Tables created successfully!")

    #Insert Sample Data
    def insert_sample_data(self):
        #Insert courses
        courses = [
            ("MSE800", "Software Engineering ", 12, 15),
            ("MSE801", "Quantum Computing", 11, 15),
            ("MSE802", "Research Methods", 11, 15)
        ]
        #Using INSERT OR REPLACE for courses to handle primary key conflicts
        self.cursor.executemany("INSERT OR REPLACE INTO Course VALUES (?, ?, ?, ?)", courses)

        #Insert students
        students = [
            (1, "Rukshan", "De Silva", "Auckland", "MSE800"),
            (2, "Kavindu", "Pahasara", "Wellington", "MSE801"),
            (3, "Vinuka", "Wimalananda", "Auckland", "MSE800")
        ]
        self.cursor.executemany("INSERT OR IGNORE INTO Student VALUES (?, ?, ?, ?, ?)", students)

        #Insert teachers
        teachers = [
            (100, "Arun", "Kumar"),
            (101, "Mohammad", "Norouzifard"),
            (102, "Saveeta", "Bai")
        ]
        self.cursor.executemany("INSERT OR IGNORE INTO Teacher VALUES (?, ?, ?)", teachers)

        #Assign students to courses
        assigns = [
            (1, "MSE800", "2025-11-07"),
            (2, "MSE801", "2025-11-10"),
            (3, "MSE802", "2025-11-17")
        ]
        self.cursor.executemany("INSERT OR IGNORE INTO Assign VALUES (?, ?, ?)", assigns)

        #Deliver: which teacher teaches which course
        delivers = [
            #Software Engineering (MSE800) taught by Mohammad (101)
            (101, "MSE800", "Morning"),
            #Quantum Computing (MSE801) taught by Arun (100)
            (100, "MSE801", "Evening"),
            #Research Methods (MSE802) taught by Saveeta (102)
            (102, "MSE802", "Afternoon"),
        ]
        #Using INSERT OR IGNORE
        self.cursor.executemany("INSERT OR IGNORE INTO Deliver VALUES (?, ?, ?)", delivers)

        self.conn.commit()
        print("Sample data inserted successfully!")

    #Query 1: List all teachers teaching MSE801
    def list_teachers_for_mse802(self):
        self.cursor.execute("""
        SELECT T_FName, T_LName
        FROM Teacher
        JOIN Deliver ON Teacher.T_ID = Deliver.T_ID
        WHERE Deliver.C_ID = 'MSE801'
        """)
        teachers = self.cursor.fetchall()
        print("\nTeachers teaching MSE801:")
        for t in teachers:
            print(f"- {t[0]} {t[1]}")

    #Query 2: Show the number of students for MSE800 course
    def count_students_for_mse800(self):
        #Using the Student table where Stu_Course is MSE800
        self.cursor.execute("""
        SELECT COUNT(Stu_ID)
        FROM Student
        WHERE Stu_Course = 'MSE800'
        """)

        count = self.cursor.fetchone()[0]
        print("\nNumber of students enrolled in MSE800:")
        print(f"- {count}")

    #Close the connection
    def close(self):
        self.conn.close()

#MAIN PROGRAM
if __name__ == "__main__":
    db = CollegeDB() #Create object

    #Clear and recreate database
    db.clear_database()
    db.create_tables()

    #Insert sample data
    db.insert_sample_data()

    #Run Queries
    db.list_teachers_for_mse802() # Query 1
    db.count_students_for_mse800() # Query 2

    db.close() #Close database