package set

type Set[T comparable] map[T]bool

func New[T comparable](slice []T) *Set[T] {
	result := Set[T]{}
	result.AddAll(slice)
	return &result
}

func (s *Set[T]) Contains(key T) bool {
	_, ok := (*s)[key]
	return ok
}

func (s *Set[T]) Add(val T) {
	(*s)[val] = true
}

func (s *Set[T]) AddAll(values []T) {
	for _, x := range values {
		s.Add(x)
	}
}

func (s *Set[T]) Remove(value T) bool {
	if s.Contains(value) {
		delete(*s, value)
		return true
	}

	return false
}

func (s *Set[T]) Pop() T {
	k := s.Peek()
	delete(*s, k)
	return k
}

func (s *Set[T]) Peek() T {
	var k T
	for k = range *s {
		break
	}
	return k
}

func (s *Set[T]) Intersection(s2 *Set[T]) *Set[T] {
	result := Set[T]{}

	for k := range *s {
		if s2.Contains(k) {
			result.Add(k)
		}
	}

	return &result
}

func (s *Set[T]) Union(s2 *Set[T]) *Set[T] {
	result := Set[T]{}
	for k := range *s {
		result.Add(k)
	}
	for k := range *s2 {
		result.Add(k)
	}
	return &result
}
