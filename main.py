import random
import time
import matplotlib.pyplot as plt


#  Insertion sort - O(n²)

def insertion_sort(nums):
    nums = nums.copy()
    for i in range(1, len(nums)):
        key = nums[i]
        j = i - 1
        while j >= 0 and nums[j] > key:
            nums[j + 1] = nums[j]
            j -= 1
        nums[j + 1] = key
    return nums



# Selection sort - O(n²)

def selection_sort(nums):
    nums = nums.copy()
    for i in range(len(nums)):
        min_idx = i
        for j in range(i + 1, len(nums)):
            if nums[j] < nums[min_idx]:
                min_idx = j
        nums[i], nums[min_idx] = nums[min_idx], nums[i]
    return nums



#  Quick sort (iterative, random pivot)

def quick_sort_iterative(nums):
    nums = nums.copy()
    stack = [(0, len(nums) - 1)]
    while stack:
        low, high = stack.pop()
        if low < high:
            pivot_idx = random.randint(low, high)
            pivot_value = nums[pivot_idx]
            i, j = low, high
            while i <= j:
                while nums[i] < pivot_value:
                    i += 1
                while nums[j] > pivot_value:
                    j -= 1
                if i <= j:
                    nums[i], nums[j] = nums[j], nums[i]
                    i += 1
                    j -= 1
            if low < j:
                stack.append((low, j))
            if i < high:
                stack.append((i, high))
    return nums



#  Shell sort

def shell_sort(nums):
    nums = nums.copy()
    n = len(nums)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = nums[i]
            j = i
            while j >= gap and nums[j - gap] > temp:
                nums[j] = nums[j - gap]
                j -= gap
            nums[j] = temp
        gap //= 2
    return nums



#  Heap sort

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

def heap_sort_v2(arr):
    arr = arr.copy()
    n = len(arr)
    for i in range(n//2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr



# Benchmark(?)

def test_speeds(functions, dataset):
    results = []
    for name, fn in functions.items():
        data_copy = dataset.copy()
        start = time.perf_counter()
        sorted_arr = fn(data_copy)
        end = time.perf_counter()
        correct = sorted_arr == sorted(dataset)
        results.append((name, round(end - start, 5), correct))
    return results



if __name__ == "__main__":
    n = 1500
    arr = [random.randint(0, 10000) for _ in range(n)]

    algos = {
        "Insertion Sort": insertion_sort,
        "Selection Sort": selection_sort,
        "Quick Sort (Iterative)": quick_sort_iterative,
        "Shell Sort": shell_sort,
        "Heap Sort": heap_sort_v2
    }

    print(f"Testing {n} elements...\n")
    results = test_speeds(algos, arr)

    print(f"{'Algorithm':28} | {'Time (s)':9} | {'Correct'}")
    print("-"*50)
    for name, t, ok in results:
        print(f"{name:28} | {t:<9} | {ok}")

    # --- Graph ---
    names = [r[0] for r in results]
    times = [r[1] for r in results]

    plt.figure(figsize=(8,5))
    plt.barh(names, times)
    plt.title(f"Sorting {n} elements — Performance (Version 2)")
    plt.xlabel("Time (seconds)")
    plt.tight_layout()
    plt.show()

    # ===========================
    # Problem 2 – Complexity Table
    # ===========================
    print("\n\n=== Problem 2: Complexity Analysis (Version 2) ===\n")
    print("| Algorithm           | Best     | Average   | Worst     | Space | Notes |")
    print("|----------------------|----------|-----------|-----------|--------|-------|")
    print("| Insertion Sort       | O(n)     | O(n²)     | O(n²)     | O(1)   | Good for small arrays |")
    print("| Selection Sort       | O(n²)    | O(n²)     | O(n²)     | O(1)   | Simple and predictable |")
    print("| Quick Sort (Iterative)| O(n log n) | O(n log n) | O(n²) | O(log n) | Faster than recursion |")
    print("| Shell Sort           | O(n log n) | O(n^(3/2)) | O(n²) | O(1) | Tunable gaps |")
    print("| Heap Sort            | O(n log n) | O(n log n) | O(n log n) | O(1) | In-place sorting |")
