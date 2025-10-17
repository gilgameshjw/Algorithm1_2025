import random
import time
from sorting.bubble import bubble_sort
from sorting.heap import heap_sort
from sorting.merge import merge_sort
from sorting.quick import quick_sort

def benchmark():
    algorithms = {
        "Bubble Sort": bubble_sort,
        "Heap Sort": heap_sort,
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort
    }

    sizes = [100, 1000, 10000]
    results = []

    for size in sizes:
        data = [random.randint(0, 100000) for _ in range(size)]
        print(f"\n=== Array size: {size} ===")

        for name, func in algorithms.items():
            start = time.perf_counter()
            _, comparisons, swaps = func(data)
            end = time.perf_counter()
            duration = end - start

            print(f"{name}: {duration:.5f}s | Comparisons: {comparisons} | Swaps: {swaps}")
            results.append((name, size, duration, comparisons, swaps))

    return results

if __name__ == "__main__":
    benchmark()
