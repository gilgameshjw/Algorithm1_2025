# exo_9_solutions.py

def count_functions(n, m):
    """
    Problem 1: Count possible functions
    F: {0,1}^n → {0,1}^m
    """
    # Number of input combinations
    input_count = 2 ** n
    
    # For output {0,1}
    if m == 1:
        return 2 ** (2 ** n)  # 2^(2^n)
    
    # For output {-1, 0, 1}
    if m == 1.5:  # Special case for ternary output
        return 3 ** (2 ** n)
    
    # For output {0,1}^m
    output_count = 2 ** m
    return output_count ** input_count  # (2^m)^(2^n) = 2^(m * 2^n)

def nand_gate(a, b):
    """
    NAND gate implementation
    """
    return 0 if (a == 1 and b == 1) else 1

def build_gates_from_nand():
    """
    Problem 2: Build AND, OR, NOT from NAND
    """
    print("Building gates from NAND:")
    print("=" * 50)
    
    # NOT from NAND: NOT A = A NAND A
    def NOT(a):
        return nand_gate(a, a)
    
    print(f"NOT(0) = {NOT(0)}")
    print(f"NOT(1) = {NOT(1)}")
    
    # AND from NAND: A AND B = NOT(A NAND B)
    def AND(a, b):
        return NOT(nand_gate(a, b))
    
    print(f"\nAND(0,0) = {AND(0,0)}")
    print(f"AND(0,1) = {AND(0,1)}")
    print(f"AND(1,0) = {AND(1,0)}")
    print(f"AND(1,1) = {AND(1,1)}")
    
    # OR from NAND: A OR B = (NOT A) NAND (NOT B)
    def OR(a, b):
        return nand_gate(NOT(a), NOT(b))
    
    print(f"\nOR(0,0) = {OR(0,0)}")
    print(f"OR(0,1) = {OR(0,1)}")
    print(f"OR(1,0) = {OR(1,0)}")
    print(f"OR(1,1) = {OR(1,1)}")
    
    return NOT, AND, OR

def universal_boolean_circuits(n):
    """
    Problem 3: Universal Boolean Circuits
    """
    explanation = f"""
    For function F: {{0,1}}^{n} → {{0,1}}:
    
    1. There are 2^n possible inputs.
    2. For each input x, we can create a delta function δ_x that outputs 1 only for that specific input.
    3. Each δ_x can be implemented with O(n) gates (using AND gates to check each bit).
    4. The function F can be expressed as:
       F(input) = OR over all x where F(x)=1 of δ_x(input)
    5. This requires at most 2^n delta functions, each of size O(n).
    6. Total circuit size: O(n * 2^n)
    
    For n = {n}:
    - Input space size: {2**n}
    - Maximum circuit size: O({n} * {2**n}) = O({n * 2**n})
    """
    return explanation

def test_problems():
    """
    Test all problems
    """
    print("Problem 1: Counting Functions")
    print("=" * 50)
    
    for n in [1, 2, 3]:
        print(f"\nFor n = {n}:")
        print(f"  Output {{0,1}}: {count_functions(n, 1)} functions")
        print(f"  Output {{-1,0,1}}: {3 ** (2 ** n)} functions")
        print(f"  Output {{0,1}}^{2}: {count_functions(n, 2)} functions")
    
    print("\n" + "=" * 50)
    print("Problem 2: NAND Universality")
    print("=" * 50)
    
    NOT, AND, OR = build_gates_from_nand()
    
    print("\n" + "=" * 50)
    print("Problem 3: Universal Boolean Circuits")
    print("=" * 50)
    
    for n in [2, 3, 4]:
        print(f"\nFor n = {n}:")
        print(universal_boolean_circuits(n))

if __name__ == "__main__":
    test_problems()
