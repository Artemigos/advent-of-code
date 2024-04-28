package main

import (
	"aoc/utils"
	"fmt"
	"strings"
)

type Op struct {
	Type string
	X1   int
	Y1   int
	X2   int
	Y2   int
}

func main() {
	lines := utils.ReadLines()
	ranges := []Op{}

	// parse data
	for _, line := range lines {
		segments := strings.Split(line, " ")
		variant := "toggle"
		iOffset := 0
		if segments[0] != "toggle" {
			variant = segments[1]
			iOffset = 1
		}
		start := segments[iOffset+1]
		end := segments[iOffset+3]
		startSegments := strings.Split(start, ",")
		endSegments := strings.Split(end, ",")
		ranges = append(ranges, Op{
			variant,
			utils.Atoi(startSegments[0]),
			utils.Atoi(startSegments[1]),
			utils.Atoi(endSegments[0]),
			utils.Atoi(endSegments[1]),
		})
	}

	// part 1
	ranges = utils.Reverse(ranges)

	lit := 0
	for x := range 1000 {
		for y := range 1000 {
			mod := 0
			found := false
			for _, r := range ranges {
				if r.X1 <= x && x <= r.X2 && r.Y1 <= y && y <= r.Y2 {
					if r.Type == "toggle" {
						mod = 1 - mod
						continue
					}
					if r.Type == "on" && mod == 0 {
						lit += 1
					} else if r.Type == "off" && mod == 1 {
						lit += 1
					}
					found = true
					break
				}
			}
			if !found {
				lit += mod
			}
		}
	}

	fmt.Println(lit)

	// part 2
	ranges = utils.Reverse(ranges)

	totalBrightness := 0
	for x := range 1000 {
		for y := range 1000 {
			brightness := 0
			for _, r := range ranges {
				if r.X1 <= x && x <= r.X2 && r.Y1 <= y && y <= r.Y2 {
					if r.Type == "toggle" {
						brightness += 2
					} else if r.Type == "on" {
						brightness += 1
					} else {
						brightness -= 1
						if brightness < 0 {
							brightness = 0
						}
					}
				}
			}
			totalBrightness += brightness
		}
	}

	fmt.Println(totalBrightness)
}
