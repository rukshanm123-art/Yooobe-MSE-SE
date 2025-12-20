


class Person:
    """
    The Base Class representing a generic person.
    Stores attributes common to everyone.
    """

    def __init__(self, p_id, name):
        self.id = p_id
        self.name = name

    def display_info(self):
        return f"ID: {self.id}, Name: {self.name}"


class Student(Person):
    """
    Child class of Person.
    Inherits 'id' and 'name' from Person, adds 'student_id'.
    """

    def __init__(self, p_id, name, student_id):
        #Call the constructor of the parent class (Person)
        super().__init__(p_id, name)
        self.student_id = student_id

    def display_info(self):
        #Extend the parent's display method
        base_info = super().display_info()
        return f"[Student] {base_info}, Student ID: {self.student_id}"


class Staff(Person):
    """
    Child class of Person.
    Inherits 'id' and 'name', adds 'staff_id' and 'tax_num'.
    """

    def __init__(self, p_id, name, staff_id, tax_num):
        super().__init__(p_id, name)
        self.staff_id = staff_id
        self.tax_num = tax_num

    def display_info(self):
        base_info = super().display_info()
        return f"{base_info}, Staff ID: {self.staff_id}, Tax : {self.tax_num}"


class General(Staff):
    """
    Child class of Staff (Grandchild of Person).
    Represents general staff members. Adds 'rate_of_pay'.
    """

    def __init__(self, p_id, name, staff_id, tax_num, rate_of_pay):
        #Initialize the immediate parent (Staff)
        super().__init__(p_id, name, staff_id, tax_num)
        self.rate_of_pay = rate_of_pay

    def display_info(self):
        #Reuse Staff's display logic
        staff_info = super().display_info()
        return f"[General Staff] {staff_info}, Pay Rate: ${self.rate_of_pay}/hr"


class Academic(Staff):
    """
    Child class of Staff.
    Represents academic staff. Adds 'publications'.
    """

    def __init__(self, p_id, name, staff_id, tax_num, publications):
        super().__init__(p_id, name, staff_id, tax_num)
        #publications is a list of strings
        self.publications = publications

    def display_info(self):
        staff_info = super().display_info()
        return f"[Academic Staff] {staff_info}, Publications: {', '.join(self.publications)}"


#Main
if __name__ == "__main__":
    print(" University Personnel System \n")

    #Create a Student
    #Uses Person constructor for name/id, stores own student_id
    s1 = Student(p_id="P001", name="Rukshan De Silva", student_id="S101")

    #Create General Staff
    #Inherits from Staff > Person
    g1 = General(p_id="P002", name="Kavindu Pahasara", staff_id="ST69", tax_num="TX-123", rate_of_pay=35)

    #Create Academic Staff
    #Inherits from Staff -> Person
    a1 = Academic(p_id="P003", name="Arun Kumar", staff_id="ST01", tax_num="TX-456",
                  publications=["Quantum Computing 101", "Advanced Quantum Theories"])

    #Displaying Data
    people = [s1, g1, a1]

    for person in people:
        print(person.display_info())