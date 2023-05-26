package main

import (
	"aoc/utils"
	"fmt"
	"strings"
)

type Guide struct {
	l string
	r string
}

func main() {
	lines := utils.ReadLines("../2022/02/data.txt")
	guide := make([]Guide, 0)

	for _, line := range lines {
		if line == "" {
			continue
		}
		segments := strings.Split(line, " ")
		guide = append(guide, Guide{segments[0], segments[1]})
	}

	fmt.Printf("%v\n", guide)

	// TODO: finish
}
