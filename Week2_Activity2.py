import math


#Recursive Fibonacci
def fib(n):
#Returns first n Fibonacci numbers using recursion only

    def helper(k, a=0, b=1, lst=[0, 1]):
        #Each call pushes a new frame on the stack with k, a, b, lst
        if k <= 0:  #base case → start popping stack
            return lst
        return helper(k - 1, b, a + b, lst + [a + b])  #push next call

    if n <= 0: return []
    if n == 1: return [0]
    return helper(n - 2)  #we already have first 2 numbers


#Recursive Factorial
def factorial(n, acc=1):
    """Recursive factorial – uses call stack to remember multiplications"""
    if n <= 1:  #deepest call → return result
        return acc  #stack starts unwinding (popping)
    return factorial(n - 1, acc * n)  #push next multiplication on stack


#Recursive input (replaces while loop)
def ask():
    try:
        n = int(input("Enter a non-negative integer N: "))
        if n >= 0:
            return n
        print("Please enter >= 0")
        return ask()  #recurse = loop again
    except ValueError:
        print("Invalid input")
        return ask()  #recurse on error


#Main
if __name__ == "__main__":
    N = ask()  # no while loop

    print(f"\nFirst {N} Fibonacci numbers:")
    print(fib(N))

    #Use our recursive version for small N, math for big N
    if N > 1000:
        print(f"\nFactorial of {N} = {math.factorial(N)} (using math for large N)")
    else:
        print(f"\nFactorial of {N} = {factorial(N)} (pure recursive)")