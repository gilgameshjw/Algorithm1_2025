# Пирамидальная сортировка (Heap Sort)
# Временная сложность: O(n log n)
# Пространственная сложность: O(1)

def heapify(arr, n, i, counters):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n:
        counters["comparisons"] += 1
        if arr[left] > arr[largest]:
            largest = left

    if right < n:
        counters["comparisons"] += 1
        if arr[right] > arr[largest]:
            largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        counters["swaps"] += 1
        heapify(arr, n, largest, counters)


def heap_sort(arr):
    n = len(arr)
    counters = {"comparisons": 0, "swaps": 0}
    a = arr.copy()

    # Построение кучи
    for i in range(n // 2 - 1, -1, -1):
        heapify(a, n, i, counters)

    # Извлечение элементов
    for i in range(n - 1, 0, -1):
        a[i], a[0] = a[0], a[i]
        counters["swaps"] += 1
        heapify(a, i, 0, counters)

    return a, counters["comparisons"], counters["swaps"]
