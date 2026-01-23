class StudentManager:
    def __init__(self, ids, names, scores):
        #W6-A1 – Part 1:
        #Dictionary 1: Student ID as key, Name as value
        self.student_names = dict(zip(ids, names))

        #Dictionary 2: Student ID as key, Score as value
        self.student_scores = dict(zip(ids, scores))

    def get_passing_students(self):
        #W6-A1 – Part 2:
        #Combine the two and filter for score >= 50
        passing_dict = {
            s_id: {"name": self.student_names[s_id], "score": self.student_scores[s_id]}
            for s_id, score in self.student_scores.items()
            if score >= 50
        }
        return passing_dict


#Data Input
ids = ["S001", "S002", "S003", "S004", "S005"]
names = ["Vinuka", "Pahasara", "Nirmal", "Rukshan", "Oshan"]
scores = [85, 42, 78, 95, 48]  # Pahasara (42) and Oshan (48) do not meet the 50% threshold

#Execution

#Initialize the object-oriented project
manager = StudentManager(ids, names, scores)

#Generate the filtered dictionary
passing_records = manager.get_passing_students()

#Final Display
print("Passing Student Records:")
for s_id, data in passing_records.items():
    print(f"ID: {s_id} | Name: {data['name']} | Score: {data['score']}")