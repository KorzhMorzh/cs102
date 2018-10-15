def is_prime(n):
    """
    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
    """
    # PUT YOUR CODE HERE
    dividers = 0
    for i in range(1,n):
        if n % i == 0:
            dividers += 1
    if dividers == 1:
        return True
    else:
        return False

