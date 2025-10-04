def school_multiplication(X, Y):
    """
    multiplying 2 big numbers, shown as list of numbers in the reverse order.

    :param X: list of numbers of 1st number (e.g., 879 -> [9, 7, 8]).
    :param Y: list of numbers of 2nd number.
    :return: result in the reverse order.
    """
    # result will have maximal length len(X) + len(Y)
    result_size = len(X) + len(Y)   # i=0 (number 9), i=1 (number 7), i=2 (number 8)
    result = [0] * result_size      # j=0 (number 2), j=1 (number 9)

    # main cycle of multiplying "in a column"
    for i in range(len(X)):
        for j in range(len(Y)):
            product = X[i] * Y[j]
            result[i + j] += product
    carry = 0
    for k in range(result_size):
        current_val = result[k] + carry
        result[k] = current_val % 10
        carry = current_val // 10
    while len(result) > 1 and result[-1] == 0:
        result.pop()

    return result


# x = 879, y = 92
x_vec = [9, 7, 8]
y_vec = [2, 9]

# 879 * 92 = 80868
product_vec = school_multiplication(x_vec, y_vec)

product_str = "".join(map(str, reversed(product_vec)))
print(f"result of multiply: {product_str}")  # output: 80868