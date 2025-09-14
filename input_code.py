def factorial(n):
    return n * factorial(n - 1)  # No base case -> Infinite recursion

print(factorial(5))
