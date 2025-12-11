package sorts

func SelectionSortInPlace(a []int) {
	n := len(a)
	for i := 0; i < n; i++ {
		minIdx := i
		for j := i + 1; j < n; j++ {
			if a[j] < a[minIdx] {
				minIdx = j
			}
		}
		a[i], a[minIdx] = a[minIdx], a[i]
	}
}

func SelectionSort(a []int) []int {
	b := append([]int(nil), a...)
	SelectionSortInPlace(b)
	return b
}
