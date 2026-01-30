"""A simple calculator module with intentional issues for practice."""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    return a / b  # BUG: no zero-division handling


def power(a, b):
    """Raise a to the power of b."""
    result = 1
    for _ in range(b):  # BUG: doesn't handle negative exponents
        result *= a
    return result


def average(numbers):
    """Calculate the average of a list of numbers."""
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)  # BUG: no empty list handling
