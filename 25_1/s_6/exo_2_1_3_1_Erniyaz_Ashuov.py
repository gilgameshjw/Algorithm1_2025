#problem 1 -  write own Quick Sort
# add random pivot

import random

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = random.choice(arr)
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]
    return quick_sort(less) + equal + quick_sort(greater)

arr = [64, 34, 25, 12, 22, 11, 90]
print(quick_sort(arr))
