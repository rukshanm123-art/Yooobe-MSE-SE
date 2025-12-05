class FileReader:
    def __init__(self, filepath):

        #Initialize with the path to the file.
        self.filepath = filepath
        self.content = ""

    def read_and_print(self):
        #Reads the file content and prints it to the console.

        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                self.content = file.read()
                print(" File Content ")
                print(self.content)
        except FileNotFoundError:
            print(f"Error: The file '{self.filepath}' was not found.")

    def count_character(self, char_to_count):
        #Counts occurrences of a specific character in the loaded content.

        count = self.content.count(char_to_count)
        print(f"\nNumber of '{char_to_count}' characters found: {count}")

#Main execution
if __name__ == "__main__":
    #Initialize the object with the filename
    analyzer = FileReader("/Users/rukshandesilva/Downloads/3280709.txt")

    #Read and print the file
    analyzer.read_and_print()

    #Count the asterisk characters
    analyzer.count_character("*")