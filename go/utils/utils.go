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

	result := strings.Split(string(data), "\n")
	if result[len(result)-1] == "" {
		result = result[:len(result)-1]
	}
	return result
}

func Sum(data []int) int {
	result := 0
	for _, x := range data {
		result += x
	}
	return result
}
