class FileReader:
    def __init__(self, filepath):
        #Initialize with the path to the file.
        self.filepath = filepath

    def append_end_of_file_message(self, message):

        #Appends a new message to the end of the file.
        #Uses the 'a' mode to ensure existing content is not overwritten.

        try:
            #Using 'a' mode for appending, which means data is added
            #to the end of the file without deleting existing content.

            with open(self.filepath, 'a', encoding='utf-8') as file:

                #Add newlines before the message for clean separation
                file.write("\n\n" + message)
                print(f" Successfully Appended Message to File: {self.filepath} ---")
        except Exception as e:
            print(f"Error appending to file: {e}")

    def read_and_print(self):

        #Reads the entire file content and prints it to the console.
        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                print("\n--- File Content (Including Appended Message) ---")
                print(content)
        except FileNotFoundError:
            print(f"Error: The file '{self.filepath}' was not found.")


#Main execution
if __name__ == "__main__":
    filepath = "/Users/rukshandesilva/Downloads/3280709.txt"

    #Define the W3-A1 End of File message
    end_message = (

        "END OF FILE\n"
        "Thank You"
    )

    #Initialize the OOP object
    analyzer = FileReader(filepath)

    #Append the "End of File" message to the file (this step does NOT overwrite)
    analyzer.append_end_of_file_message(end_message)

    #Read and print the entire file content (with the appended message)
    analyzer.read_and_print()