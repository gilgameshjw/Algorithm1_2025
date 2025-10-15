# Problem 3 (Compare Sorting Algorithms)
import random
import time

def bad_sort(arr):
    for i in range(len(arr)):
        for j in range(0, len(arr)-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = random.choice(arr)
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]
    return quick_sort(less) + equal + quick_sort(greater)

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def heap_sort(arr):
    def heapify(arr, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and arr[l] > arr[largest]:
            largest = l
        if r < n and arr[r] > arr[largest]:
            largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr

def time_sort_algorithm(sort_func, arr):
    start = time.time()
    sort_func(arr)
    end = time.time()
    return end - start

arr = [random.randint(1, 1000) for _ in range(1000)]

bubble_sort_time = time_sort_algorithm(bad_sort, arr.copy())
quick_sort_time = time_sort_algorithm(quick_sort, arr.copy())
merge_sort_time = time_sort_algorithm(merge_sort, arr.copy())
heap_sort_time = time_sort_algorithm(heap_sort, arr.copy())

print(f"Bubble sort time: {bubble_sort_time} seconds")
print(f"Quick sort time: {quick_sort_time} seconds")
print(f"Merge sort time: {merge_sort_time} seconds")
print(f"Heap sort time: {heap_sort_time} seconds")
