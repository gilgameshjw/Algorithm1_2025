def bad_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                # Swap
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

print(bad_sort([100, 50, 75, 25, 0])) 


#-----Quick Sort------

def quick_sort_random(arr):
    if len(arr) <= 1:
        return arr
    pivot = random.choice(arr)
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort_random(left) + mid + quick_sort_random(right)

#-----Merge Sort------

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr)//2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

print(merge_sort([100, 50, 75, 25, 0])) 


#-----Heap Sort------

def heapify(arr, n, i):
    largest = i        
    left = 2 * i + 1   
    right = 2 * i + 2  

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0] 
        heapify(arr, i, 0)                

    return arr


print(heap_sort([100, 50, 75, 25, 0]))