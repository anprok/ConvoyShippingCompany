import sys

recursion_limit = sys.getrecursionlimit()
print(recursion_limit)  # 1000
sys.setrecursionlimit(200)
new_limit = sys.getrecursionlimit()
print(new_limit)