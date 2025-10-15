#problem1
def divide(v, left, right):
    if left == right:
        if v[left] == 1:
            return left
        else:
            return -1

    mid = (left + right) // 2
    left_result = divide(v, left, mid)
    
    if left_result != -1:
        return left_result
    
    return divide(v, mid + 1, right)

v = [0, 0, 0, 1, 0, 0, 0]
result = divide(v, 0, len(v) - 1)

if result != -1:
    print(f"position '1' is: {result}")
else:
    print("No '1' found")
