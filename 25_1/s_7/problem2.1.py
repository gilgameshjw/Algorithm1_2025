def school_multiplication(X, Y):
    """
    Implements the standard school multiplication algorithm (base 10).
    X and Y are lists of digits, where X[0] is the least significant digit (LSD).
    Complexity: O(nx * ny) = O(n^2)
    """
    nx = len(X)
    ny = len(Y)
    # The result R can have up to nx + ny digits.
    R = [0] * (nx + ny) 

    # Outer loop: Iterate through each digit of Y (j)
    for j in range(ny):
        carry = 0
        # Inner loop: Multiply Y[j] by each digit of X (i)
        for i in range(nx):
            # 1. Digit multiplication + add existing R[i+j] + add carry
            # Note: We work from right-to-left (i.e., X[i] is 10^i)
            product = X[i] * Y[j] + R[i + j] + carry
            
            # 2. Separate digit and carry
            R[i + j] = product % 10
            carry = product // 10
            
        # 3. Handle final carry for the current row
        R[nx + j] += carry
        
    # Remove leading zeros (most significant zeros)
    while len(R) > 1 and R[-1] == 0:
        R.pop()

    return R

def list_to_int(d_list):
    """Converts a list of digits (LSD first) back to an integer for display."""
    return int("".join(map(str, d_list[::-1])))

# --- Примеры использования ---
num1 = 1234
num2 = 567

# Convert integers to lists of digits (LSD first)
X = [int(d) for d in str(num1)][::-1] # [4, 3, 2, 1]
Y = [int(d) for d in str(num2)][::-1] # [7, 6, 5]

R_digits = school_multiplication(X, Y)
result_int = list_to_int(R_digits)

print("\n--- School Multiplication (O(n^2)) ---")
print(f"X: {X} (Value: {num1})")
print(f"Y: {Y} (Value: {num2})")
print(f"Result Digits (R): {R_digits} (Value: {result_int})")
print(f"Verification: {num1 * num2}")