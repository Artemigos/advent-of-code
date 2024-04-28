package main

import (
	"aoc/utils"
	"fmt"
	"regexp"
	"slices"
	"strings"
)

type (
	Op     func([]*int) int
	Values map[string]int
	Gate   struct {
		inputs []string
		op     Op
		output string
	}
)

func bitNot(val []*int) int {
	return *val[0] ^ 0b1111111111111111
}

func passthrough(val []*int) int {
	return *val[0]
}

func getVal(v Values, valSpec string) *int {
	if matched, _ := regexp.MatchString("\\d+", valSpec); matched {
		r := new(int)
		*r = utils.Atoi(valSpec)
		return r
	} else if _, ok := v[valSpec]; ok {
		r := new(int)
		*r = v[valSpec]
		return r
	}
	return nil
}

func setVal(values Values, name string, val int) {
	values[name] = val
	if name == "a" {
		fmt.Println(val)
	}
}

func propagateVal(v Values, gates []Gate, name string) {
	fulfilled := []Gate{}
	for _, g := range gates {
		if slices.Contains(g.inputs, name) {
			if _, ok := v[g.output]; !ok {
				vals := utils.Map(g.inputs, func(s string) *int { return getVal(v, s) })
				valsNotNone := utils.Map(vals, func(i *int) bool { return i != nil })
				if !utils.All(valsNotNone) {
					continue
				}
				result := g.op(vals)
				setVal(v, g.output, result)
				fulfilled = append(fulfilled, g)
			}
		}
	}

	for _, g := range fulfilled {
		propagateVal(v, gates, g.output)
	}
}

func opForName(name string) Op {
	if name == "AND" {
		return func(v []*int) int { return *v[0] & *v[1] }
	} else if name == "OR" {
		return func(v []*int) int { return *v[0] | *v[1] }
	} else if name == "LSHIFT" {
		return func(v []*int) int { return *v[0] << *v[1] }
	} else { // RSHIFT
		return func(v []*int) int { return *v[0] >> *v[1] }
	}
}

func main() {
	lines := utils.ReadLines()

	values := make(Values)
	gates := []Gate{}

	for _, line := range lines {
		segments := strings.Split(line, " ")
		name := segments[len(segments)-1]
		if len(segments) == 3 { // just a value provided
			gates = append(gates, Gate{[]string{segments[0]}, passthrough, name})
			val := getVal(values, segments[0])
			if val != nil {
				setVal(values, name, *val)
				propagateVal(values, gates, name)
			}
		} else if len(segments) == 4 { // NOT
			gates = append(gates, Gate{[]string{segments[1]}, bitNot, name})
			val := getVal(values, segments[1])
			if val != nil {
				setVal(values, name, bitNot([]*int{val}))
				propagateVal(values, gates, name)
			}
		} else { // two-arg operators
			op := opForName(segments[1])
			gates = append(gates, Gate{[]string{segments[0], segments[2]}, op, name})
			val1 := getVal(values, segments[0])
			val2 := getVal(values, segments[2])
			if val1 != nil && val2 != nil {
				setVal(values, name, op([]*int{val1, val2}))
				propagateVal(values, gates, name)
			}
		}
	}

	// part 2
	aVal := values["a"]
	values = make(Values)
	values["b"] = aVal

	for _, g := range gates {
		if _, ok := values[g.output]; !ok {
			vals := utils.Map(g.inputs, func(s string) *int { return getVal(values, s) })
			valsNotNone := utils.Map(vals, func(i *int) bool { return i != nil })
			if !utils.All(valsNotNone) {
				continue
			}
			result := g.op(vals)
			setVal(values, g.output, result)
			propagateVal(values, gates, g.output)
		}
	}
}
