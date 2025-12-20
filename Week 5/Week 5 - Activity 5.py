




#The Root Parent Class
class Animal:
    def __init__(self, name):
        self.name = name

    def display_info(self):
        return f"Animal Name: {self.name}"


#Intermediate Classes (Inherit from Animal)
class Mammal(Animal):
    def __init__(self, name, feature="Has Fur"):
        super().__init__(name)  #Pass name to Animal
        self.feature = feature


class Bird(Animal):
    def __init__(self, name, feature="Has Feathers"):
        super().__init__(name)
        self.feature = feature


class Fish(Animal):
    def __init__(self, name, feature="Has Gills"):
        super().__init__(name)
        self.feature = feature


#Concrete Classes (Inherit from Level 2)

#Mammal Children
class Dog(Mammal):
    def walk(self):
        print(f"🐕 {self.name} ({self.feature}) is trying to save Penny.")


class Cat(Mammal):
    def walk(self):
        print(f"🐈 {self.name} ({self.feature}) is very agile.")


#Bird - Children
class Eagle(Bird):
    def fly(self):
        print(f"🦅 {self.name} ({self.feature}) is flexing his wings.")


class Penguin(Bird):
    def swim(self):
        print(f"🐧 {self.name} ({self.feature}) is swimming in Madagascar waters.")


#Fish - Children
class Salmon(Fish):
    def swim(self):
        print(f"🐟 {self.name} ({self.feature}) is trying to find his family.")


class Shark(Fish):
    def swim(self):
        print(f"🦈 {self.name} ({self.feature}) is trying to find a pray.")


#Main
if __name__ == "__main__":
    print("Animals Inheritance Demo\n")

    #Create instances of the classes
    my_dog = Dog("Bolt")
    my_cat = Cat("Simba")
    my_eagle = Eagle("The Mighty Eagle")
    my_penguin = Penguin("Kowalsky")
    my_salmon = Salmon("Nemo")
    my_shark = Shark("The Great White")

    #Demonstrate behaviors defined in the diagram
    my_dog.walk()
    my_cat.walk()
    print("-" * 30)

    my_eagle.fly()
    my_penguin.swim()
    print("-" * 30)

    my_salmon.swim()
    my_shark.swim()