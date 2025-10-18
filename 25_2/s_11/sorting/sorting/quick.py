# Быстрая сортировка (Quick Sort)
# Средняя сложность: O(n log n)
# Худшая: O(n²)
# Пространственная сложность: O(log n)

def quick_sort(arr, counters=None):
    if counters is None:
        counters = {"comparisons": 0, "swaps": 0}
    a = arr.copy()
    _quick_sort(a, 0, len(a) - 1, counters)
    return a, counters["comparisons"], counters["swaps"]

def _quick_sort(a, low, high, counters):
    if low < high:
        p = partition(a, low, high, counters)
        _quick_sort(a, low, p - 1, counters)
        _quick_sort(a, p + 1, high, counters)

def partition(a, low, high, counters):
    pivot = a[high]
    i = low - 1
    for j in range(low, high):
        counters["comparisons"] += 1
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
            counters["swaps"] += 1
    a[i + 1], a[high] = a[high], a[i + 1]
    counters["swaps"] += 1
    return i + 1
