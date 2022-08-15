def rec_sum(n):
    return n if n < 2 else n + rec_sum(n - 1)