#Using the built-in math package for factorial

import math  #built-in package


def fibonacci(n):
    """
    Same simple Fibonacci function as in Part 1
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]

    fib_series = [0, 1]
    for i in range(2, n):
        next_number = fib_series[i - 1] + fib_series[i - 2]
        fib_series.append(next_number)

    return fib_series


#Now I replace my own factorial function with math.factorial


#Main program
if __name__ == "__main__":
    while True:
        try:
            N = int(input("Enter a positive integer N: "))
            if N >= 0:
                break
            else:
                print("Please enter a number >= 0")
        except ValueError:
            print("Please enter a valid integer")

    #Fibonacci (unchanged)
    fib_list = fibonacci(N)
    print(f"\nFirst {N} Fibonacci numbers:")
    print(fib_list)

    #Factorial using math package
    #math.factorial raises ValueError for negative numbers, so we need to catch it
    try:
        fact = math.factorial(N)
        print(f"\nFactorial of {N} = {fact}   (calculated with math.factorial)")
    except ValueError:
        print(f"\nFactorial of {N} is not defined (negative number)")