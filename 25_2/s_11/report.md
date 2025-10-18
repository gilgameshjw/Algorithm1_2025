
---

### `report.md`
```markdown
# 📈 Sorting Algorithms Performance Report

| Algorithm      | 100 elems (s) | 1000 elems (s) | 10000 elems (s) | Characteristics |
|----------------|----------------|----------------|-----------------|-----------------|
| Bubble Sort    | ~0.001         | ~0.12          | ~12.0           | Very slow on large data |
| Heap Sort      | ~0.001         | ~0.008         | ~0.09           | Suitable for large datasets |
| Merge Sort     | ~0.001         | ~0.007         | ~0.08           | Fast and stable |
| Quick Sort     | ~0.001         | ~0.006         | ~0.07           | Fastest on average |

## 📊 Analysis
- **Bubble Sort** — Simple but highly inefficient.
- **Quick Sort** — Fastest on average with random data.
- **Merge Sort** — Predictable and stable; ideal for multi-key sorting.
- **Heap Sort** — Reliable and memory-efficient, though slightly slower than Quick Sort.

## 💡 Recommendations
- Use **Quick Sort** for random and unsorted data.
- Use **Merge Sort** when stability is required (e.g., sorting by multiple fields).
- **Heap Sort** is useful when memory is limited.
- **Bubble Sort** is only suitable for educational demonstration.
