# Сортировка слиянием (Merge Sort)
# Временная сложность: O(n log n)
# Пространственная сложность: O(n)

def merge(left, right, counters):
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        counters["comparisons"] += 1
        if left[i] < right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
            counters["swaps"] += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def merge_sort(arr, counters=None):
    if counters is None:
        counters = {"comparisons": 0, "swaps": 0}
    if len(arr) <= 1:
        return arr, counters["comparisons"], counters["swaps"]

    mid = len(arr) // 2
    left, _, _ = merge_sort(arr[:mid], counters)
    right, _, _ = merge_sort(arr[mid:], counters)
    merged = merge(left, right, counters)

    return merged, counters["comparisons"], counters["swaps"]
