import random
import time
import matplotlib.pyplot as plt


# 1. Bubble Sort (O(n^2))

def bubble_sort(arr):
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr



# 2. Quick Sort (Random Pivot)

def quick_sort_random(arr):
    if len(arr) <= 1:
        return arr
    pivot = random.choice(arr)
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort_random(left) + middle + quick_sort_random(right)



# 3. Quick Sort (Median Pivot)

def median_of_three(a, b, c):
    return sorted([a, b, c])[1]

def quick_sort_median(arr):
    if len(arr) <= 1:
        return arr
    pivot = median_of_three(arr[0], arr[len(arr)//2], arr[-1])
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort_median(left) + middle + quick_sort_median(right)



# 4. Merge Sort

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr)//2
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



# 5. Heap Sort

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
    arr = arr.copy()
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    return arr



# 6. Benchmark function

def benchmark(sort_functions, data):
    results = []
    for name, func in sort_functions.items():
        start = time.perf_counter()
        sorted_data = func(data.copy())
        end = time.perf_counter()
        results.append((name, round(end - start, 5), sorted_data == sorted(data)))
    return results



# MAIN

if __name__ == "__main__":
    n = 2000  
    data = [random.randint(0, 10000) for _ in range(n)]

    sort_algorithms = {
        "Bubble Sort (O(n^2))": bubble_sort,
        "Quick Sort (Random Pivot)": quick_sort_random,
        "Quick Sort (Median Pivot)": quick_sort_median,
        "Merge Sort": merge_sort,
        "Heap Sort": heap_sort
    }

    print(f"Sorting {n} elements...\n")
    results = benchmark(sort_algorithms, data)

    print(f"{'Algorithm':35} | {'Time (s)':10} | {'Correct'}")
    print("-"*55)
    for name, t, correct in results:
        print(f"{name:35} | {t:<10} | {correct}")

    # Plot results
    names = [r[0] for r in results]
    times = [r[1] for r in results]

    plt.figure(figsize=(8,5))
    plt.bar(names, times)
    plt.xticks(rotation=20)
    plt.title(f"Sorting {n} elements — Performance Comparison")
    plt.ylabel("Time (seconds)")
    plt.tight_layout()
    plt.show()

    
    # Problem 2 — Complexity Analysis
    
    print("\n\n=== Problem 2: Time and Space Complexity Analysis ===\n")
    print("| Algorithm                | Best Case   | Average Case | Worst Case  | Space Complexity | Notes |")
    print("|---------------------------|-------------|---------------|-------------|------------------|-------|")
    print("| Bubble Sort              | O(n)        | O(n²)         | O(n²)       | O(1)             | Simple but slow |")
    print("| Quick Sort (Random Pivot)| O(n log n)  | O(n log n)    | O(n²)       | O(log n)         | Fast, not stable |")
    print("| Quick Sort (Median Pivot)| O(n log n)  | O(n log n)    | O(n log n)  | O(log n)         | Improved pivot choice |")
    print("| Merge Sort               | O(n log n)  | O(n log n)    | O(n log n)  | O(n)             | Stable, predictable |")
    print("| Heap Sort                | O(n log n)  | O(n log n)    | O(n log n)  | O(1)             | In-place, not stable |")
