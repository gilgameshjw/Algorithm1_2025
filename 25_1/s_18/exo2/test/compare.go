package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"time"

	"exo2/sorts"
)

func isSorted(a []int) bool {
	for i := 1; i < len(a); i++ {
		if a[i-1] > a[i] {
			return false
		}
	}
	return true
}

func genData(n int, seed int64) []int {
	r := seed
	a := make([]int, n)
	for i := range a {
		r = (1103515245*r + 12345) & 0x7fffffff
		a[i] = int(r%2001) - 1000
	}
	return a
}

type algo struct {
	name string
	fn   func([]int) []int
}

func timeOnce(name string, fn func([]int) []int, data []int) time.Duration {
	start := time.Now()
	out := fn(data)
	d := time.Since(start)
	if !isSorted(out) {
		panic(name + " produced unsorted output")
	}
	return d
}

func main() {
	algs := []algo{
		{"Bad (SelectionSort)", sorts.SelectionSort},
		{"QuickSort (random)", sorts.QuickSortRandom},
		{"QuickSort (median3)", sorts.QuickSortMedian3},
		{"MergeSort", sorts.MergeSort},
		{"HeapSort", sorts.HeapSort},
	}
	sizes := []int{1_000, 5_000, 10_000, 20_000}

	fmt.Printf("%-22s | %8s | %10s\n", "Algorithm", "n", "time (ms)")
	fmt.Println("--------------------------------------------")

	type row struct {
		Alg string
		N   int
		Ms  float64
	}
	var rows []row

	for _, n := range sizes {
		data := genData(n, 42)
		for _, a := range algs {
			best := time.Duration(0)
			for r := 0; r < 3; r++ {
				d := timeOnce(a.name, a.fn, data)
				if r == 0 || d < best {
					best = d
				}
			}
			ms := float64(best.Microseconds()) / 1000.0
			fmt.Printf("%-22s | %8d | %10.3f\n", a.name, n, ms)
			rows = append(rows, row{a.name, n, ms})
		}
	}

	f, err := os.Create("compare_results.csv")
	if err == nil {
		defer f.Close()
		w := csv.NewWriter(f)
		defer w.Flush()
		_ = w.Write([]string{"algorithm", "n", "time_ms"})
		for _, r := range rows {
			_ = w.Write([]string{r.Alg, fmt.Sprint(r.N), fmt.Sprintf("%.3f", r.Ms)})
		}
		fmt.Println("\nCSV saved to compare_results.csv")
	} else {
		fmt.Println("\nWARNING:", err)
	}
}
