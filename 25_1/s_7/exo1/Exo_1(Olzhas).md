Problem 1 Sparse Vector Search

// v - исходный вектор, start - начальный индекс, end - конечный индекс
function FIND_ONE_BIN(v, start, end):
    // Базовый случай: поддиапазон размера 1
    if start == end:
        if v[start] == 1:
            return start // Найдена '1'
        else:
            return -1  // '1' не найдена в этом листе

    // Базовый случай для остановки рекурсии 
    if start > end:
        return -1

    // Шаг разделения: найти середину
    mid = floor((start + end) / 2)

    // Шаг завоевания: рекурсивный вызов для левой половины
    index_left = FIND_ONE_BIN(v, start, mid)

    // Шаг объединения:
    // Если '1' найдена в левой половине, возвращаем её.
    if index_left != -1:
        return index_left

    // Иначе, рекурсивный вызов для правой половины
    index_right = FIND_ONE_BIN(v, mid + 1, end)

    // Возвращаем результат из правой половины
    return index_right

// Начальный вызов: FIND_ONE_BIN(v, 0, n - 1)
Problem 2: School Multiplication

function SCHOOL_MULTIPLICATION(X, Y, nx, ny):
    // P - результирующий массив, инициализированный нулями. Размер: nx + ny
    P = array of size (nx + ny) initialized to 0

    // Итерация по каждой цифре второго числа Y (множитель)
    for j from 0 to ny - 1:
        carry = 0
        // Итерация по каждой цифре первого числа X (множимое)
        for i from 0 to nx - 1:
            // Умножение одной цифры и добавление предыдущего переноса
            product = X[i] * Y[j] + P[i + j] + carry

            // Сохранение цифры в результирующем массиве
            P[i + j] = product mod 10

            // Новый перенос
            carry = floor(product / 10)

        // Сохранение последнего переноса
        P[nx + j] = carry

    // Определение фактической длины результата (удаление ведущих нулей)
    len_P = nx + ny
    while len_P > 1 and P[len_P - 1] == 0:
        len_P = len_P - 1

    return P
