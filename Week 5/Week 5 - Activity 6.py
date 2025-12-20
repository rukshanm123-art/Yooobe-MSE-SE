#Image 1 - Logic
class Person:
    def __init__(self, name, address, age):
        # Encapsulation: Using a single underscore denotes a 'protected' variable
        self._name = name
        self.address = address
        self.age = age

    def greet(self):
        # The parent version of the method
        print("Greetings and felicitations from the maestro " + self._name)


#image 2 - Logic
class Student(Person):
    def __init__(self, name, address, age, student_id):
        #Inheritance: Initialize attributes using the parent's constructor
        super().__init__(name, address, age)
        self.student_id = student_id

    def greet(self):
        #Method Overriding: Changing the behavior for the child class
        print("Hi " + self._name)


#Demonstration
if __name__ == "__main__":
    person1 = Person("Dr. Smith", "456 University Way", 50)
    student1 = Student("Alice", "123 Main St", 20, "S12345")

    print("Executing person1.greet():")
    person1.greet()

    print("\nExecuting student1.greet():")
    student1.greet()