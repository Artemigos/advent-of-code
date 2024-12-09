package utils

import (
	"os"
	"strconv"
	"strings"
)

func getPath() string {
	if len(os.Args) != 2 {
		panic("data file path required")
	}
	return os.Args[1]
}

func Read() string {
	path := getPath()
	data, err := os.ReadFile(path)
	if err != nil {
		panic(err)
	}

	result, _ := strings.CutSuffix(string(data), "\n")
	return result
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

func Atoi(s string) int {
	num, err := strconv.Atoi(s)
	if err != nil {
		panic(err)
	}
	return num
}

func AsInts(list []string) []int {
	return Map(list, Atoi)
}

func Map[TFrom any, TTo any](from []TFrom, mapper func(TFrom) TTo) []TTo {
	result := make([]TTo, len(from))
	for i, f := range from {
		result[i] = mapper(f)
	}
	return result
}

func All(arr []bool) bool {
	for _, b := range arr {
		if !b {
			return false
		}
	}
	return true
}

func Any(arr []bool) bool {
	for _, b := range arr {
		if b {
			return true
		}
	}

	return false
}

func Abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}
