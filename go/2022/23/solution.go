package main

import (
	"aoc/utils"
	"aoc/utils/set"
)

type Pos struct {
	x, y int
}

func main() {
	lines := utils.ReadLines()
	elves := set.Set[Pos]{}
	for y, line := range lines {
		for x, c := range []rune(line) {
			if c == '#' {
				elves.Add(Pos{x, y})
			}
		}
	}

	currElves := elves
	i := 0
	for {
		moved := false
		moves := map[Pos]Pos{}
		destinations := map[Pos]int{}
		for e := range currElves {
			move := chooseMove(i, currElves, e.x, e.y)
			if move != nil {
				moves[e] = *move
				destinations[*move] += 1
			}
		}

		newElves := set.Set[Pos]{}
		for e := range currElves {
			m, ok := moves[e]
			if !ok || destinations[m] > 1 {
				newElves.Add(e)
			} else {
				newElves.Add(m)
				moved = true
			}
		}

		currElves = newElves
		i += 1

		// part 1
		if i == 10 {
			e := currElves.Peek()
			minX, maxX, minY, maxY := e.x, e.x, e.y, e.y
			for p := range currElves {
				if p.x < minX {
					minX = p.x
				}
				if p.x > maxX {
					maxX = p.x
				}
				if p.y < minY {
					minY = p.y
				}
				if p.y > maxY {
					maxY = p.y
				}
			}

			println((maxX-minX+1)*(maxY-minY+1) - len(elves))
		}

		if !moved {
			break
		}
	}

	// part 2
	println(i)
}

func chooseMove(i int, elves set.Set[Pos], x int, y int) *Pos {
	// TODO
	neighbors := []Pos{
		{x - 1, y - 1},
		{x, y - 1},
		{x + 1, y - 1},
		{x + 1, y},
		{x + 1, y + 1},
		{x, y + 1},
		{x - 1, y + 1},
		{x - 1, y},
	}

	found := false
	for _, n := range neighbors {
		if elves.Contains(n) {
			found = true
			break
		}
	}

	if !found {
		return nil
	}

	dirs := [][]Pos{
		neighbors[:3],
		neighbors[4:7],
		append(append([]Pos{}, neighbors[6:]...), neighbors[:1]...),
		neighbors[2:5],
	}

	dir_results := []Pos{
		{x, y - 1},
		{x, y + 1},
		{x - 1, y},
		{x + 1, y},
	}

	for di := range dirs {
		idx := (i + di) % len(dirs)
		all := true
		for _, p := range dirs[idx] {
			if elves.Contains(p) {
				all = false
				break
			}
		}

		if all {
			return &dir_results[idx]
		}
	}

	return nil
}
