package main

import (
	"aoc/utils"
	"aoc/utils/set"
)

func main() {
	lines := utils.ReadLines()

	// part 1
	acc := 0
	for _, line := range lines {
		if line == "" {
			continue
		}
		middle := len(line) / 2
		left, right := line[:middle], line[middle:]
		common := set.New([]rune(left)).Intersection(set.New([]rune(right)))
		if len(*common) != 1 {
			panic(len(*common))
		}
		acc += score(common.Pop())
	}

	println(acc)

	// part 2
	acc = 0
	for i := 0; i < len(lines); i += 3 {
		s1 := set.New([]rune(lines[i]))
		s2 := set.New([]rune(lines[i+1]))
		s3 := set.New([]rune(lines[i+2]))
		common := s1.Intersection(s2).Intersection(s3)
		if len(*common) != 1 {
			panic(len(*common))
		}
		acc += score(common.Pop())
	}

	println(acc)
}

func score(letter rune) int {
	if letter >= 'a' {
		return int(letter - 'a' + 1)
	} else {
		return int(letter - 'A' + 27)
	}
}
