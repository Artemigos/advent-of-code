package main

import (
	"aoc/utils"
)

func main() {
	lines := utils.ReadLines("../2022/03/data.txt")

	// part 1
	acc := 0
	for _, line := range lines {
		if line == "" {
			continue
		}
		middle := len(line) / 2
		left, right := line[:middle], line[middle:]
		common := set([]rune(left)).intersect(set([]rune(right)))
		if len(*common) != 1 {
			panic(len(*common))
		}
		acc += scoreLetter(*common.pop())
	}

	println(acc)

	// part 2
	acc = 0
	for i := 0; i < len(lines); i += 3 {
		s1 := set([]rune(lines[i]))
		s2 := set([]rune(lines[i+1]))
		s3 := set([]rune(lines[i+2]))
		common := s1.intersect(s2).intersect(s3)
		if len(*common) != 1 {
			panic(len(*common))
		}
		acc += scoreLetter(*common.pop())
	}

	println(acc)
}

func scoreLetter(letter rune) int {
	if letter >= 'a' {
		return int(letter - 'a' + 1)
	} else {
		return int(letter - 'A' + 27)
	}
}

// dirty Set implementation

type Set[T comparable] map[T]bool

func (s *Set[T]) intersect(s2 *Set[T]) *Set[T] {
	result := Set[T]{}

	for k := range *s {
		if _, ok := (*s2)[k]; ok {
			result[k] = true
		}
	}

	return &result
}

func set[T comparable](slice []T) *Set[T] {
	result := Set[T]{}
	for _, x := range slice {
		result[x] = true
	}
	return &result
}

func (s *Set[T]) pop() *T {
	for k := range *s {
		return &k
	}

	return nil
}
