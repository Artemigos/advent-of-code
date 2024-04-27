package main

import (
	"aoc/utils"
	"crypto/md5"
	"fmt"
	"strconv"
)

func main() {
	data := utils.Read()
	found5 := false
	found6 := false
	five := 0
	six := 0

	i := 0
	for {
		i++
		hash := md5.New()
		hash.Write([]byte(data))
		hash.Write([]byte(strconv.Itoa(i)))
		sum := hash.Sum(nil)

		if !found5 && sum[0] == 0 && sum[1] == 0 && sum[2]&0xF0 == 0 {
			found5 = true
			five = i
		}

		if !found6 && sum[0] == 0 && sum[1] == 0 && sum[2] == 0 {
			found6 = true
			six = i
		}

		if found5 && found6 {
			break
		}
	}

	fmt.Println(five)
	fmt.Println(six)
}
