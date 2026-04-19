```python
def factorial(n):
    # Check if input is an integer
    if not isinstance(n, int):
        raise TypeError("Input must be an integer.")
    # Check if input is non-negative
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")
    # Base case: 0! or 1! is 1
    if n == 0 or n == 1:
        return 1
    # Recursive case: n! = n * (n-1)!
    return n * factorial(n - 1)

print(factorial(5))
```