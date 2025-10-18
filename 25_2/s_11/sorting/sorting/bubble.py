def bubble_sort(arr):
    n = len(arr)
    comparisons = 0
    swaps = 0
    a = arr.copy()

    for i in range(n - 1):
        for j in range(n - i - 1):
            comparisons += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1

    return a, comparisons, swaps
