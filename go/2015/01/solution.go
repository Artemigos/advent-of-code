package main

import (
	"aoc/utils"
	"fmt"
)

func main() {
	data := utils.Read()
	floor := 0
	firstBasementAt := 0
	for i, c := range data {
		if c == '(' {
			floor += 1
		} else {
			floor -= 1
		}

		if floor < 0 && firstBasementAt == 0 {
			firstBasementAt = i + 1
		}
	}

	fmt.Println(floor)
	fmt.Println(firstBasementAt)
}
