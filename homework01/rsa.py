import random


def is_prime(n: int) -> bool:
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
    for i in range(1, n):
        if n % i == 0:
            dividers += 1
    if dividers == 1:
        return True
    else:
        return False


def gcd(a: int, b: int) -> int:
    """
    >>> gcd(12, 15)
    3
    >>> gcd(3, 7)
    1
    """
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a


def multiplicative_inverse(e: int, phi: int) -> int:
    """
    >>> multiplicative_inverse(7, 40)
    23
    """
    a = [phi]
    b = [e]
    a_mod_b = [phi % e]
    a_div_b = [phi // e]
    x = [0]
    y = [1]
    i = 0
    while a[i] % b[i] != 0:
        a.append(b[i])
        b.append(a_mod_b[i])
        a_mod_b.append(a[i + 1] % b[i + 1])
        a_div_b.append(a[i+1] // b[i+1])
        i += 1
    for j in range(1, len(a)):
        x.append(y[j-1])
        y.append(x[j-1] - y[j-1]*a_div_b[len(a)-j-1])
    d = y[len(a)-1] % phi
    return d


def generate_keypair(p: int, q: int) -> tuple:
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')

    # n = pq
    n = p*q
    # phi = (p-1)(q-1)
    phi = (p-1)*(q-1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)
    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))
