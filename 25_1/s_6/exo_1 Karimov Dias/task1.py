def find_one_recursive(v, start, end, m):
    """
    recursively searching for 1 un submassive v[start:end+1].

    :param v: entering vector (list).
    :param start: initial index of current submassive.
    :param end: last index of current submassive.
    :param m: quantity of parts for divison (2 for binary division).
    :return: index '1', if found, or else -1.
    """
    if start == end:
        if v[start] == 1:
            return start
        else:
            return -1
    result = -1
    sub_array_size = (end - start + 1) // m

    for i in range(m):
        sub_start = start + i * sub_array_size
        sub_end = sub_start + sub_array_size - 1 if i < m - 1 else end

        # recursiv call for submassive
        if sub_start <= sub_end:
            found_index = find_one_recursive(v, sub_start, sub_end, m)
            if found_index != -1:
                result = found_index
                break  # if found, exiting from cycle

    return result

n = 100
pos = 42
vector = [0] * n
vector[pos] = 1

print(f"Бинарное деление (m=2): Найдена '1' на позиции {find_one_recursive(vector, 0, len(vector) - 1, 2)}")
print(f"Тернарное деление (m=3): Найдена '1' на позиции {find_one_recursive(vector, 0, len(vector) - 1, 3)}")

# master's theorem:
# recurrent relation will be: T(n) = m * T(n/m) + O(1)

"D part"
def find_one_linear(v):
    for i in range(len(v)):
        if v[i] == 1:
            return i

#result: of course, simple approach is the beast because recursive method creates tree by dividding everything on 2, whereas simple approach just goes linearly by whole massive.
#conclusion: divide&conquer is a powerful tool, but not universal. it fits best when we are able to discard big amount of data. when we need to check whole massive with each element, simple approach is the best.