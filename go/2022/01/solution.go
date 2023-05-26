package main

import (
	"aoc/utils"
	"sort"
	"strconv"
)

func main() {
	lines := utils.ReadLines("../2022/01/data.txt")

	currentElf := 0
	elves := make([]int, 0)

	for _, line := range lines {
		if line == "" {
			elves = append(elves, currentElf)
			currentElf = 0
		} else {
			val, err := strconv.Atoi(line)
			if err != nil {
				panic(err)
			}
			currentElf += val
		}
	}

	if currentElf > 0 {
		elves = append(elves, currentElf)
	}

	sort.Ints(elves)
	println(elves[len(elves)-1])

	part2 := utils.Sum(elves[len(elves)-3:])
	println(part2)
}
