import random

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    # merge
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


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)


def heap_sort(arr):
    def heapify(array, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n and array[left] > array[largest]:
            largest = left
        if right < n and array[right] > array[largest]:
            largest = right
        
        if largest != i:
            array[i], array[largest] = array[largest], array[i]
            heapify(array, n, largest)
    
    n = len(arr)
    
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    
    return arr


def selection_sort(arr):
    n = len(arr)
    
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    
    return arr


# ============================================
# TESTING
# ============================================

# Generate random arrays
random_num = random.sample(range(1, 50), 8)

print("SORTING ALGORITHMS TEST")

# Test
print("\nTest: Random array")
print("Original: ", random_num)
print("Merge Sort:", merge_sort(random_num.copy()))
print("Quick Sort:", quick_sort(random_num.copy()))
print("Heap Sort: ", heap_sort(random_num.copy()))
print("Selection: ", selection_sort(random_num.copy()))

print("Done!")