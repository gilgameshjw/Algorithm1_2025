import random

# ==============================================================================
# PROBLEM 1: SPARSE VECTOR SEARCH (O(n) Divide and Conquer)
# ==============================================================================

def contains_one(v, start, end):
    """
    Helper function to check if the '1' is in the sub-range [start, end].
    COST: O(k) where k = end - start + 1. This O(n) cost makes the DC search O(n) overall.
    """
    for i in range(start, end + 1):
        if v[i] == 1:
            return True
    return False

def find_one_dc_sparse(v, start=0, end=None, level=0):
    """
    Binary Divide and Conquer search for the single '1'.
    Complexity: O(n) due to O(n) check in the filter step.
    
    NOTE: Added 'level' for optional visualization of recursion.
    """
    if end is None:
        end = len(v) - 1

    # Base Case: Single element remaining
    if start == end:
        # print(f"{'  ' * level}Base Case: Found '1' at index {start}")
        return start if v[start] == 1 else -1

    # Divide
    mid = (start + end) // 2
    
    # Optional: Visualization of current step
    # print(f"{'  ' * level}Dividing range [{start}, {end}]. Check left [{start}, {mid}]")

    # Conquer/Filter (The O(n) cost happens inside contains_one)
    if contains_one(v, start, mid):
        return find_one_dc_sparse(v, start, mid, level + 1)
    else:
        # '1' must be in the right half [mid + 1, end]
        # print(f"{'  ' * level}Moving right to [{mid + 1}, {end}]")
        return find_one_dc_sparse(v, mid + 1, end, level + 1)

# Simple O(n) approach for comparison (Problem 1d)
def find_one_simple(v):
    """Simple linear scan (O(n))."""
    for i, val in enumerate(v):
        if val == 1:
            return i
    return -1


# ==============================================================================
# RANDOMIZED EXAMPLE USAGE WITH FULL OUTPUT
# ==============================================================================

VECTOR_SIZE = 20
# 1. Generate a random index for the '1'
random_index = random.randint(0, VECTOR_SIZE - 1)

# 2. Create the sparse vector
v_example_random = [0] * VECTOR_SIZE
v_example_random[random_index] = 1

# --- Output and Execution ---
print("=" * 70)
print("PROBLEM 1: SPARSE VECTOR SEARCH")
print(f"Vector size: {VECTOR_SIZE}")
print(f"Random '1' Position (Actual): {random_index}")
print("-" * 70)

# ⭐️ FULL ARRAY OUTPUT
print("Generated Vector V (Index: Value):")
# Выводим индексы для удобства
print("Index:  ", "  ".join(f"{i % 10:2}" for i in range(VECTOR_SIZE)))
print("Value:  ", "  ".join(f"{v:2}" for v in v_example_random))
print("-" * 70)

# 1. Divide and Conquer search
index_dc = find_one_dc_sparse(v_example_random)
print(f"Result (Divide and Conquer O(n)): {index_dc}")

# 2. Simple linear search
index_simple = find_one_simple(v_example_random)
print(f"Result (Simple Linear Scan O(n)): {index_simple}")

print(f"\nVerification: Both results match the actual position: {index_dc == random_index}")
print("=" * 70)