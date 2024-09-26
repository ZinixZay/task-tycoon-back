import string


rows = [str(i) for i in range(1, 101)]

columns = []
for i in range(1, 26 * 3 + 1):
    column = ''
    while i > 0:
        i -= 1
        column = string.ascii_uppercase[i % 26] + column
        i //= 26
    columns.append(column)
