#problem 1 - 3 part 2 
# Quick Sort with Average Pivot (Down + Middle + Up)
def average_pivot(arr):
    if len(arr) <= 1:
        return arr
    low = arr[0]
    mid = arr[len(arr) // 2]
    high = arr[-1]
    pivot = sorted([low, mid, high])[1]
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]
    return average_pivot(less) + equal + average_pivot(greater)

arr = [64, 34, 25, 12, 22, 11, 90]
print(average_pivot(arr))
