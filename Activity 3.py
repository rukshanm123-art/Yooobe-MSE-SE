def fibonacci(n):
    """
    Generates a list with the first n Fibonacci numbers.
    """
    if n <= 0:
        return []  #return empty list if n is 0 or negative
    elif n == 1:
        return [0]  #first 1 number → [0]

    fib_series = [0, 1]  #start with the first two numbers
    for i in range(2, n):
        next_number = fib_series[i - 1] + fib_series[i - 2]  #add last two numbers
        fib_series.append(next_number)

    return fib_series  #return the complete list


def factorial(n):
    """
    Calculates factorial of n (n!) using a loop.
    """
    if n < 0:
        return None  #factorial is not defined for negative numbers
    if n == 0 or n == 1:
        return 1

    result = 1
    for i in range(2, n + 1):
        result = result * i  #multiply sequentially
    return result


#Main program
if __name__ == "__main__":
    #Ask the user for a positive integer
    while True:
        try:
            N = int(input("Enter a positive integer N: "))
            if N >= 0:
                break
            else:
                print("Please enter a number >= 0")
        except ValueError:
            print("Please enter a valid integer")

    #Generate Fibonacci series
    fib_list = fibonacci(N)
    print(f"\nFirst {N} Fibonacci numbers:")
    print(fib_list)

    #Compute factorial
    fact = factorial(N)
    if fact is None:
        print(f"\nFactorial of {N} is not defined (negative number)")
    else:
        print(f"\nFactorial of {N} = {fact}")

 