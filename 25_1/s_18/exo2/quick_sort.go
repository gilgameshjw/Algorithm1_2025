package main

import (
	"exo2/sorts"
	"fmt"
	"math/rand"
	"time"
)

func clone(a []int) []int {
	b := make([]int, len(a))
	copy(b, a)
	return b
}

func quickSortRandom(a []int) {
	rand.Seed(time.Now().UnixNano())
	qsRandom(a, 0, len(a)-1)
}

func qsRandom(a []int, lo, hi int) {
	if lo >= hi {
		return
	}
	p := partitionRandom(a, lo, hi)
	qsRandom(a, lo, p-1)
	qsRandom(a, p+1, hi)
}

func partitionRandom(a []int, lo, hi int) int {
	pivotIdx := lo + rand.Intn(hi-lo+1)
	a[pivotIdx], a[hi] = a[hi], a[pivotIdx]
	pivot := a[hi]

	i := lo
	for j := lo; j < hi; j++ {
		if a[j] <= pivot {
			a[i], a[j] = a[j], a[i]
			i++
		}
	}
	a[i], a[hi] = a[hi], a[i]
	return i
}

func quickSortMedian3(a []int) {
	qsMedian3(a, 0, len(a)-1)
}

func qsMedian3(a []int, lo, hi int) {
	if lo >= hi {
		return
	}
	p := partitionMedian3(a, lo, hi)
	qsMedian3(a, lo, p-1)
	qsMedian3(a, p+1, hi)
}

func partitionMedian3(a []int, lo, hi int) int {
	mid := lo + (hi-lo)/2

	if a[mid] < a[lo] {
		a[lo], a[mid] = a[mid], a[lo]
	}
	if a[hi] < a[lo] {
		a[lo], a[hi] = a[hi], a[lo]
	}
	if a[hi] < a[mid] {
		a[mid], a[hi] = a[hi], a[mid]
	}

	a[mid], a[hi] = a[hi], a[mid]
	pivot := a[hi]

	i := lo
	for j := lo; j < hi; j++ {
		if a[j] <= pivot {
			a[i], a[j] = a[j], a[i]
			i++
		}
	}
	a[i], a[hi] = a[hi], a[i]
	return i
}

func main() {
	a := []int{10, 6, 2, 1, 5, 8, 3, 4, 7, 9}

	fmt.Println("Result (QuickSort - random):     ", sorts.QuickSortRandom(a))
	fmt.Println("Result (QuickSort - median3):    ", sorts.QuickSortMedian3(a))
}
