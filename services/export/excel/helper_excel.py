import string
from typing import List


rows: List[str] = [str(i) for i in range(1, 101)]

columns: List[str] = []
for i in range(1, 26 * 3 + 1):
    column = ''
    while i > 0:
        i -= 1
        column = string.ascii_uppercase[i % 26] + column
        i //= 26
    columns.append(column)
