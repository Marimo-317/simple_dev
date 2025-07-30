def fibonacci(n):
    """
    Generate the first n numbers in the Fibonacci sequence.
    
    Args:
        n (int): Number of Fibonacci numbers to generate
        
    Returns:
        list: Array of first n Fibonacci numbers
        
    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    elif n == 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib_sequence = [0, 1]
    for i in range(2, n):
        fib_sequence.append(fib_sequence[i-1] + fib_sequence[i-2])
    
    return fib_sequence


if __name__ == "__main__":
    # Example usage
    print("Fibonacci sequence examples:")
    for i in [0, 1, 5, 10]:
        print(f"fibonacci({i}) = {fibonacci(i)}")
