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
	lines := utils.ReadLines()
	guide := make([]Guide, 0)

	for _, line := range lines {
		if line == "" {
			continue
		}
		segments := strings.Split(line, " ")
		guide = append(guide, Guide{segments[0], segments[1]})
	}

	// part 1
	score := 0
	for _, g := range guide {
		score += cScore(g.l, g.r)
	}

	fmt.Println(score)

	// part 2
	score = 0
	for _, g := range guide {
		score += cScore(change(g.l, g.r))
	}

	fmt.Println(score)
}

func cScore(l string, r string) int {
	score := 0

	switch r {
	case "X":
		score += 1
		switch l {
		case "A":
			score += 3
		case "C":
			score += 6
		}
	case "Y":
		score += 2
		switch l {
		case "B":
			score += 3
		case "A":
			score += 6
		}
	case "Z":
		score += 3
		switch l {
		case "C":
			score += 3
		case "B":
			score += 6
		}
	}

	return score
}

func change(l string, r string) (string, string) {
	switch r {
	case "X":
		switch l {
		case "A":
			r = "Z"
		case "B":
			r = "X"
		default:
			r = "Y"
		}
	case "Y":
		switch l {
		case "A":
			r = "X"
		case "B":
			r = "Y"
		default:
			r = "Z"
		}
	default:
		switch l {
		case "A":
			r = "Y"
		case "B":
			r = "Z"
		default:
			r = "X"
		}
	}

	return l, r
}
