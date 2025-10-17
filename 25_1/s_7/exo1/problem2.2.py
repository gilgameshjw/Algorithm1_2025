import math

# ==============================================================================
# PROBLEM 2.2: KARATSUBA ALGORITHM (O(n^1.585))
# ==============================================================================

def list_to_int(d_list):
    """
    Converts a list of digits (LSD first) back to an integer.
    E.g., [4, 3, 2, 1] -> 1234
    """
    if not d_list:
        return 0
    # Reverse the list and join the digits to form the number string
    return int("".join(map(str, d_list[::-1])))

def add_lists(A, B):
    """Adds two digit lists (LSD first), handling carries."""
    n = max(len(A), len(B))
    R = [0] * (n + 1)
    carry = 0
    
    # Pad A and B for consistent access
    A_padded = A + [0] * (n - len(A))
    B_padded = B + [0] * (n - len(B))
    
    for i in range(n):
        val = A_padded[i] + B_padded[i] + carry
        R[i] = val % 10
        carry = val // 10
    
    R[n] = carry
    # Remove leading zeros (most significant zeros)
    while len(R) > 1 and R[-1] == 0:
        R.pop()
    return R

def subtract_lists(A, B):
    """
    Subtracts B from A (A - B). Assumes A >= B based on Karatsuba's logic.
    """
    n = max(len(A), len(B))
    R = [0] * n
    
    # Pad B with zeros so it has length n
    B_padded = B + [0] * (n - len(B))
    
    borrow = 0
    for i in range(n):
        # Current digit of A, with borrow applied
        a_i = A[i] - borrow
        b_i = B_padded[i]
        
        if a_i < b_i:
            # Need to borrow 10 from the next position
            R[i] = a_i + 10 - b_i
            borrow = 1
        else:
            R[i] = a_i - b_i
            borrow = 0
            
    # Remove leading zeros
    while len(R) > 1 and R[-1] == 0:
        R.pop()
    return R if R else [0]


def karatsuba_multiplication(X, Y):
    """
    Implements Karatsuba's multiplication algorithm.
    Complexity: O(n^log2(3)) approx O(n^1.585)
    X and Y are lists of digits (LSD first).
    """
    n = max(len(X), len(Y))

    # --- Base Case ---
    # Switch to direct multiplication for small numbers (e.g., n < 10)
    if n < 10: 
        val_x = list_to_int(X)  # <-- Now defined!
        val_y = list_to_int(Y)
        result_int = val_x * val_y
        
        # Convert result back to list of digits (LSD first)
        if result_int == 0:
            return [0]
        return [int(d) for d in str(result_int)][::-1]

    # Pad X and Y with leading zeros to make length even (n)
    if n % 2 != 0:
        n += 1
        
    X += [0] * (n - len(X))
    Y += [0] * (n - len(Y))
    
    m = n // 2
    
    # Split: X = x1 * 10^m + x0  and Y = y1 * 10^m + y0
    x0 = X[:m]
    x1 = X[m:]
    y0 = Y[:m]
    y1 = Y[m:]
    
    # --- Three recursive calls (Multiplication steps) ---
    z0 = karatsuba_multiplication(x0, y0)
    z2 = karatsuba_multiplication(x1, y1)
    
    # z3 = (x1 + x0) * (y1 + y0)
    x_sum = add_lists(x1, x0)
    y_sum = add_lists(y1, y0)
    z3 = karatsuba_multiplication(x_sum, y_sum)
    
    # --- Middle term: z1 = z3 - z2 - z0 ---
    temp = subtract_lists(z3, z2)
    z1 = subtract_lists(temp, z0)
    
    # --- Final Result: R = z2 * 10^2m + z1 * 10^m + z0 ---
    
    # z2 * 10^2m (shift z2 by n=2m positions)
    term2 = [0] * n + z2 
    
    # z1 * 10^m (shift z1 by m positions)
    term1 = [0] * m + z1
    
    # Sum the three terms: z0 + term1 + term2
    result = add_lists(z0, term1)
    result = add_lists(result, term2)
    
    return result

# ==============================================================================
# EXAMPLE USAGE
# ==============================================================================
num1 = 987654321098765432101
num2 = 123456789123456789123

# Convert integers to lists of digits (LSD first)
X_k = [int(d) for d in str(num1)][::-1]
Y_k = [int(d) for d in str(num2)][::-1]

R_karatsuba = karatsuba_multiplication(X_k, Y_k)
result_karatsuba_int = list_to_int(R_karatsuba)

print("--- Karatsuba Multiplication (O(n^1.585)) ---")
print(f"Num1: {num1} (Length: {len(X_k)})")
print(f"Num2: {num2} (Length: {len(Y_k)})")
print(f"Result Value (Karatsuba): {result_karatsuba_int}")
print(f"Verification (Python * operator): {num1 * num2}")
print(f"Result Matches: {result_karatsuba_int == num1 * num2}")
print("-" * 50)