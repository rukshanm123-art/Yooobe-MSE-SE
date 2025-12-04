class TemperatureConverter:
    def convert(self, text):
        try:
            #Extract prefix and numeric value
            prefix, value = text[0], float(text[1:])

            if prefix == 'F':
                celsius = (value - 32) * 5 / 9
                return f"{text} degrees Fahrenheit is converted to {celsius:.2f} degrees Celsius"
            elif prefix == 'C':
                fahrenheit = (value * 9 / 5) + 32
                return f"{text} degrees Celsius is converted to {fahrenheit:.2f} degrees Fahrenheit"

        except (ValueError, IndexError):
            #Catch errors if input is too short or doesn't contain a valid number
            pass

        return "Invalid input. Please enter the temperature with the correct 'C' or 'F' prefix."


if __name__ == "__main__":
    #Create the object
    converter = TemperatureConverter()

    #Get input and print the result
    user_input = input("Enter temperature (e.g., F51, C11): ")
    print(converter.convert(user_input))