#problem2
def multiply_vectors(X, Y):
    n = len(X)
    result = [0] * (2 * n)
    
    for i in range(n):
        for j in range(n):
            result[i + j] += X[i] * Y[j]
    
    for i in range(2 * n - 1):
        if result[i] >= 10:
            result[i + 1] += result[i] // 10
            result[i] %= 10
    
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    
    return result

def print_result(result):
    print("".join(map(str, result[::-1])))

X = [1, 2, 3]
Y = [4, 5, 6]
result = multiply_vectors(X, Y)
print_result(result)
