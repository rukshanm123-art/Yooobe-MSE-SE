import sqlite3


class StudentManager:
    def __init__(self, ids, names, scores):

        #Part 1: Dictionary Setup
        self.student_names = dict(zip(ids, names))
        self.student_scores = dict(zip(ids, scores))

        #Database Integration
        self.conn = sqlite3.connect(":memory:")  #Using memory for demo, use 'students.db' for a file
        self.cursor = self.conn.cursor()
        self._setup_database()

    def _setup_database(self):

        #Creates table and inserts data from the dictionaries
        self.cursor.execute('''CREATE TABLE students 
                             (student_id TEXT, name TEXT, score INTEGER)''')

        #Preparing data from dictionaries for SQL insertion
        student_data = [
            (s_id, self.student_names[s_id], self.student_scores[s_id])
            for s_id in self.student_names
        ]

        self.cursor.executemany("INSERT INTO students VALUES (?, ?, ?)", student_data)
        self.conn.commit()

    def get_passing_students(self):

        #Part 2: Filter logic using dictionary comprehension
        passing_dict = {
            s_id: {"name": self.student_names[s_id], "score": self.student_scores[s_id]}
            for s_id, score in self.student_scores.items()
            if score >= 50
        }
        return passing_dict

    def display_top_three(self):

        #Retrieves and displays the top 3 students using an SQL query
        print("\n--- Top 3 Students (SQL Query) ---")
        query = "SELECT name, score FROM students ORDER BY score DESC LIMIT 3"
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        for i, (name, score) in enumerate(results, 1):
            print(f"{i}. {name} with a score of {score}")


#Data Input
ids = ["S1", "S2", "S3", "S4", "S5"]
names = ["Vinuka", "Pahasara", "Nirmal", "Rukshan", "Oshan"]
scores = [85, 42, 78, 95, 48]

#Execution
manager = StudentManager(ids, names, scores)

#Display Passing Students (Dictionary Condition)
passing_records = manager.get_passing_students()
print("Passing Student Records (from Dictionary):")
for s_id, data in passing_records.items():
    print(f"ID: {s_id} | Name: {data['name']} | Score: {data['score']}")

#Display Top 3 Students (Database Condition)
manager.display_top_three()