import math

def permutaciones(n, r):
    return math.factorial(n) // math.factorial(n - r)

def combinaciones(n, r):
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))