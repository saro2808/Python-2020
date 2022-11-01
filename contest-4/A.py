def pascal_triangle():
    n = 0
    C = 1
    yield 1
    while True:
        for k in range(n + 1):
            if k != n:
                C = C * (n - k) // (k + 1)
                yield C
            else:
                yield 1
        n += 1

