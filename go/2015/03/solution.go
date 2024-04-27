package main

import (
	"aoc/utils"
	"aoc/utils/set"
	"fmt"
)

type Point struct {
	X int
	Y int
}

func main() {
	data := utils.Read()

	pos1 := Point{0, 0}
	pos2 := []Point{
		{0, 0},
		{0, 0},
	}
	posI := 0
	seen1 := set.New[Point]([]Point{pos1})
	seen2 := set.New[Point]([]Point{pos2[posI]})

	for _, move := range data {
		if move == '<' {
			pos1.X -= 1
			pos2[posI].X -= 1
		} else if move == '>' {
			pos1.X += 1
			pos2[posI].X += 1
		} else if move == 'v' {
			pos1.Y += 1
			pos2[posI].Y += 1
		} else {
			pos1.Y -= 1
			pos2[posI].Y -= 1
		}
		seen1.Add(pos1)
		seen2.Add(pos2[posI])
		posI = 1 - posI
	}

	fmt.Println(len(*seen1))
	fmt.Println(len(*seen2))
}
