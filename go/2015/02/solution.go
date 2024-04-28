package main

import (
	"aoc/utils"
	"fmt"
	"strings"
)

func main() {
	lines := utils.ReadLines()

	var areaAcc, ribbonAcc int
	areaAcc = 0
	ribbonAcc = 0

	for _, line := range lines {
		segments := strings.Split(line, "x")
		sides := utils.AsInts(segments)

		area1 := sides[0] * sides[1]
		area2 := sides[0] * sides[2]
		area3 := sides[1] * sides[2]

		minArea := min(area1, area2, area3)
		areaAcc += 2*area1 + 2*area2 + 2*area3 + minArea

		perimeter1 := 2*sides[0] + 2*sides[1]
		perimeter2 := 2*sides[0] + 2*sides[2]
		perimeter3 := 2*sides[1] + 2*sides[2]

		minPerimeter := min(perimeter1, perimeter2, perimeter3)
		volume := sides[0] * sides[1] * sides[2]

		ribbonAcc += minPerimeter + volume
	}

	fmt.Println(areaAcc)
	fmt.Println(ribbonAcc)
}
