package main

import (
	"exo2/sorts"
	"fmt"
)

func selectionSort(a []int) {
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

func main() {
	a := []int{10, 6, 2, 1, 5, 8, 3, 4, 7, 9}
	sorts.SelectionSortInPlace(a)
	fmt.Println("Result (SelectionSort):", a)
}
