package main

import (
	"exo2/sorts"
	"fmt"
)

func mergeSort(items []int) []int {

	if len(items) < 2 {
		return items
	}

	left := mergeSort(items[:len(items)/2])
	right := mergeSort(items[len(items)/2:])

	return merge(left, right)

}

func merge(a []int, b []int) []int {
	final := []int{}
	i := 0
	j := 0

	for i < len(a) && j < len(b) {
		if a[i] < b[j] {
			final = append(final, a[i])
			i++
		} else {
			final = append(final, b[j])
			j++
		}
	}

	for ; i < len(a); i++ {
		final = append(final, a[i])
	}

	for ; j < len(b); j++ {
		final = append(final, b[j])
	}
	return final
}

func main() {
	a := []int{10, 6, 2, 1, 5, 8, 3, 4, 7, 9}
	sorted := sorts.MergeSort(a)
	fmt.Println("Result (MergeSort):", sorted)
}
