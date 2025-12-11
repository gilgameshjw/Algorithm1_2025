package sorts

func MergeSort(items []int) []int {
	n := len(items)
	if n < 2 {
		return append([]int(nil), items...)
	}
	mid := n / 2
	left := MergeSort(items[:mid])
	right := MergeSort(items[mid:])
	return merge(left, right)
}

func merge(a, b []int) []int {
	out := make([]int, 0, len(a)+len(b))
	i, j := 0, 0
	for i < len(a) && j < len(b) {
		if a[i] <= b[j] {
			out = append(out, a[i])
			i++
		} else {
			out = append(out, b[j])
			j++
		}
	}
	out = append(out, a[i:]...)
	out = append(out, b[j:]...)
	return out
}
