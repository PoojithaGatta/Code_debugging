```python
def factorial(n):
    # Check if n is less than 0 and raise a ValueError if true
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    # Base case: if n is 0 or 1, return 1
    elif n == 0 or n == 1:  
        return 1
    # Recursive case: n * factorial(n - 1)
    else:
        return n * factorial(n - 1)

# Test the function with different inputs
print(factorial(5))  # Expected output: 120
print(factorial(0))  # Expected output: 1
print(factorial(1))  # Expected output: 1
try:
    print(factorial(-1))  # Expected output: ValueError
except ValueError as e:
    print(e)  # Output: Factorial is not defined for negative numbers
```