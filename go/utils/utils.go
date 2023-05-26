package utils

import (
	"os"
	"strings"
)

func ReadLines(path string) []string {
	data, err := os.ReadFile(path)
	if err != nil {
		panic(err)
	}

	return strings.Split(string(data), "\n")
}

func Sum(data []int) int {
	result := 0
	for _, x := range data {
		result += x
	}
	return result
}
