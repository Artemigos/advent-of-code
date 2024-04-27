package utils

import (
	"os"
	"strings"
)

func getPath() string {
	if len(os.Args) != 2 {
		panic("data file path required")
	}
	return os.Args[1]
}

func ReadLines() []string {
	path := getPath()
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
