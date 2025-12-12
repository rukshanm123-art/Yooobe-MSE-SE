
class MathCalculator:
    #a class to calculate factorial and Fibonacci.

    def factorial(self, n):
        #Calculates the factorial of a non-negative integer n using recursion.

        #param n: The non-negative integer.
        #return: The factorial of n.

        if not isinstance(n, int) or n < 0:
            return "Error: Factorial requires a non-negative integer."

        if n == 0:
            return 1
        #call the method recursively using self.factorial
        return n * self.factorial(n - 1)

    def fibonacci(self, n):
        #calculates the n-th Fibonacci number using recursion.

        #param n: The position in the series (non-negative integer).
        #return: The n-th Fibonacci number.

        if not isinstance(n, int) or n < 0:
            return "Error: Fibonacci requires a non-negative integer."

        if n <= 1:
            return n

        #call the method recursively using self.fibonacci
        return self.fibonacci(n - 1) + self.fibonacci(n - 2)


if __name__ == "__main__":
    #create an object of the MathSeriesCalculator class
    calculator = MathCalculator()

    print("Choose an option:")
    print("1. Factorial")
    print("2. Fibonacci")

    choice = input("Enter choice (1/2): ")
    ans = "" #initialize ans

    if choice == "1" or choice == "2":
        try:
            #ask the user for the number needed for the function
            num_input = input("Enter the number (n): ")
            n = int(num_input)

            if choice == "1":
                #call the factorial method on the 'calculator' object
                ans = calculator.factorial(n)
            elif choice == "2":
                #call the fibonacci method on the 'calculator' object
                ans = calculator.fibonacci(n)
        except ValueError:
            ans = "Invalid input for the number. Please enter an integer."
        except RecursionError:
            ans = "Error: Input too large for recursive calculation."
    else:
        ans = "Invalid choice"

    print("\nFinal result:", ans)

