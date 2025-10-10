

import random
import time
import matplotlib.pyplot as plt
from typing import List, Callable

# PROBLEM 1: SORTING ALGORITHMS

def bad_sort(arr: List[int]) -> List[int]:
    """Bubble Sort - O(n²)"""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def quick_sort_random(arr: List[int]) -> List[int]:
    """Quick Sort with random pivot"""
    if len(arr) <= 1:
        return arr
    pivot = random.choice(arr)
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort_random(left) + middle + quick_sort_random(right)

def quick_sort_median(arr: List[int]) -> List[int]:
    """Quick Sort with median-of-three pivot"""
    if len(arr) <= 1:
        return arr
    first, middle, last = arr[0], arr[len(arr)//2], arr[-1]
    pivot = sorted([first, middle, last])[1]
    left = [x for x in arr if x < pivot]
    middle_list = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort_median(left) + middle_list + quick_sort_median(right)

def merge_sort(arr: List[int]) -> List[int]:
    """Merge Sort - O(n log n)"""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left: List[int], right: List[int]) -> List[int]:
    """Merge helper for merge sort"""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def heap_sort(arr: List[int]) -> List[int]:
    """Heap Sort - O(n log n)"""
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr

def heapify(arr: List[int], n: int, i: int):
    """Heapify helper for heap sort"""
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

# =============================================================================
# PROBLEM 2: ALGORITHM ANALYSIS
# =============================================================================

def analyze_algorithms():
    """Complexity analysis using Master Theorem"""
    print("COMPLEXITY ANALYSIS:")
    print("Bad Sort: O(n²) - Not divide & conquer")
    print("Quick Sort: T(n) = 2T(n/2) + O(n) → O(n log n)")
    print("Merge Sort: T(n) = 2T(n/2) + O(n) → O(n log n)")
    print("Heap Sort: O(n log n) - Not recursive D&C")

# PROBLEM 3: PERFORMANCE COMPARISON

def compare_performance():
    """Compare practical performance"""
    algorithms = {
        "Bad Sort": bad_sort,
        "Quick Sort (Random)": quick_sort_random,
        "Quick Sort (Median)": quick_sort_median,
        "Merge Sort": merge_sort,
        "Heap Sort": heap_sort
    }

    sizes = [100, 500, 1000, 2000]
    results = {name: [] for name in algorithms.keys()}

    print("\nPERFORMANCE COMPARISON (ms):")
    print(f"{'Size':<8} {'Bad Sort':<12} {'Quick(R)':<12} {'Quick(M)':<12} {'Merge':<12} {'Heap':<12}")
    print("-" * 80)

    for size in sizes:
        test_data = [random.randint(1, 10000) for _ in range(size)]
        size_results = []

        for name, algorithm in algorithms.items():
            data_copy = test_data.copy()
            start_time = time.time()
            algorithm(data_copy)
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000
            results[name].append(execution_time)
            size_results.append(execution_time)

        print(f"{size:<8} {size_results[0]:<12.2f} {size_results[1]:<12.2f} {size_results[2]:<12.2f} {size_results[3]:<12.2f} {size_results[4]:<12.2f}")

    # Create plot
    plt.figure(figsize=(10, 6))
    for name, times in results.items():
        plt.plot(sizes, times, marker='o', label=name)
    plt.xlabel('Array Size')
    plt.ylabel('Execution Time (ms)')
    plt.title('Sorting Algorithms Performance')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('sorting_performance.png', dpi=300, bbox_inches='tight')
    plt.show()

    return results

# TESTING

def test_algorithms():
    """Test that all algorithms work correctly"""
    test_cases = [
        [5, 2, 8, 1, 9],
        [3, 1, 4, 1, 5],
        [1],
        []
    ]

    algorithms = [bad_sort, quick_sort_random, merge_sort, heap_sort]
    names = ["Bad Sort", "Quick Sort", "Merge Sort", "Heap Sort"]

    print("TESTING ALGORITHMS:")
    for i, algo in enumerate(algorithms):
        passed = True
        for test in test_cases:
            result = algo(test.copy())
            expected = sorted(test.copy())
            if result != expected:
                passed = False
                break
        status = "PASS" if passed else "FAIL"
        print(f"{names[i]}: {status}")

# MAIN EXECUTION

if __name__ == "__main__":
    print("Sorting Algorithms - Problem Set #2-#3")

    # Test algorithms
    test_algorithms()

    # Analyze complexities
    analyze_algorithms()

    # Compare performance
    compare_performance()