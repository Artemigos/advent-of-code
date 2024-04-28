package main

import (
	"aoc/utils"
	"fmt"
	"strings"
)

func main() {
	lines := utils.ReadLines()
	vowels := "aeiou"

	// part 1
	niceNum := 0
	for _, line := range lines {
		vowelsNum := 0
		if strings.Contains(line, "ab") || strings.Contains(line, "cd") || strings.Contains(line, "pq") || strings.Contains(line, "xy") {
			continue
		}

		lastC := '\u0000'
		reapeatedCSatisfied := false

		for _, c := range line {
			if strings.Contains(vowels, string(c)) {
				vowelsNum++
			}
			if !reapeatedCSatisfied && c == lastC {
				reapeatedCSatisfied = true
			}
			lastC = c
		}

		if reapeatedCSatisfied && vowelsNum >= 3 {
			niceNum++
		}
	}

	fmt.Println(niceNum)

	// part 2
	niceNum = 0
	for _, line := range lines {
		pattern1Found := false
		for i := range len(line) - 3 {
			for j := i + 2; j < len(line)-1; j++ {
				if line[i] == line[j] && line[i+1] == line[j+1] {
					pattern1Found = true
					break
				}
			}
			if pattern1Found {
				break
			}
		}

		pattern2Found := false
		for i := range len(line) - 2 {
			if line[i] == line[i+2] {
				pattern2Found = true
				break
			}
		}

		if pattern1Found && pattern2Found {
			niceNum += 1
		}
	}

	fmt.Println(niceNum)
}
