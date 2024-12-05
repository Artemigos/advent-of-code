package deque

import "fmt"

type Deque[T comparable] struct {
	buf     []T
	lOffset int
	len     int
}

func New[T comparable]() *Deque[T] {
	result := &Deque[T]{
		buf:     make([]T, 3),
		lOffset: 0,
		len:     0,
	}
	return result
}

func (d *Deque[T]) Append(val T) {
	capacity := len(d.buf)
	if d.len == capacity {
		buf := make([]T, capacity*2)
		if d.lOffset+d.len <= capacity {
			copy(buf, d.buf)
		} else {
			lenBefore := len(d.buf[d.lOffset:])
			lenAfter := d.len - lenBefore
			copy(buf, d.buf[d.lOffset:])
			copy(buf[lenBefore:], d.buf[:lenAfter])
			d.lOffset = 0
		}
		d.buf = buf
		capacity *= 2
	}
	idx := (d.lOffset + d.len) % capacity
	d.buf[idx] = val
	d.len += 1
}

func (d *Deque[T]) PopLeft() (T, error) {
	var x T
	if d.len == 0 {
		return x, fmt.Errorf("Cannot pop from empty Deque.")
	}

	val := d.buf[d.lOffset]
	d.buf[d.lOffset] = x
	d.lOffset += 1
	d.lOffset %= len(d.buf)
	d.len -= 1

	if d.len == 0 {
		d.lOffset = 0
	}

	return val, nil
}

func (d *Deque[T]) Len() int {
	return d.len
}
