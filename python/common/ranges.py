from typing import Iterator, List, overload
import itertools

class ranges:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, stop: "ranges") -> None: ...
    @overload
    def __init__(self, start: int, stop: int) -> None: ...
    @overload
    def __init__(self, rng: range) -> None: ...
    @overload
    def __init__(self, rng: List[range]) -> None: ...

    def __init__(self, first = None, stop = None):
        if isinstance(first, list) and stop is None:
            for r in first:
                assert r.step == 1, 'Only ranges with step == 1 are supported.'
            self._ranges = first
            return

        if isinstance(first, range) and stop is None:
            assert first.step == 1, 'Only ranges with step == 1 are supported.'
            self._ranges = [first]
            return

        if first is None and stop is None:
            self._ranges = []
            return

        if isinstance(first, int) and stop is None:
            self._ranges = [range(first)]
            return

        if isinstance(first, int) and isinstance(stop, int):
            self._ranges = [range(first, stop)]
            return

        raise TypeError('invalid arguments')

    @overload
    def intersection(self, rng: "ranges") -> "ranges": ...
    @overload
    def intersection(self, rng: range) -> "ranges": ...

    def intersection(self, rng) -> "ranges":
        if isinstance(rng, ranges):
            curr = ranges()
            for r1 in self._ranges:
                for r2 in rng._ranges:
                    inter = range(max(r1.start, r2.start), min(r1.stop, r2.stop))
                    if len(inter) > 0:
                        curr = curr.union(inter)
            return curr

        if isinstance(rng, range):
            assert rng.step == 1, 'Only ranges with step == 1 are supported.'
            new_rng = []
            for r in self._ranges:
                inter = range(max(r.start, rng.start), min(r.stop, rng.stop))
                if len(inter) > 0:
                    new_rng.append(inter)
            return ranges(new_rng)

        raise TypeError('invalid arguments')

    @overload
    def union(self, rng: "ranges") -> "ranges": ...
    @overload
    def union(self, rng: range) -> "ranges": ...

    def union(self, rng) -> "ranges":
        if isinstance(rng, ranges):
            curr = self
            for r in rng._ranges:
                curr = curr.union(r)
            return curr

        if isinstance(rng, range):
            assert rng.step == 1, 'Only ranges with step == 1 are supported.'
            new_rng = []
            total_min, total_max = rng.start, rng.stop
            for r in self._ranges:
                inter = range(max(r.start, rng.start), min(r.stop, rng.stop))
                if len(inter) > 0:
                    total_min = min(total_min, r.start)
                    total_max = max(total_max, r.stop)
                else:
                    new_rng.append(r)
            new_rng.append(range(total_min, total_max))
            return ranges(new_rng)

        raise TypeError('invalid arguments')

    @overload
    def difference(self, rng: "ranges") -> "ranges": ...
    @overload
    def difference(self, rng: range) -> "ranges": ...

    def difference(self, rng) -> "ranges":
        if isinstance(rng, ranges):
            curr = self
            for r in rng._ranges:
                curr = curr.difference(r)
            return curr

        if isinstance(rng, range):
            assert rng.step == 1, 'Only ranges with step == 1 are supported.'
            new_rng = []
            for r in self._ranges:
                if r.stop <= rng.start or r.start >= rng.stop:
                    new_rng.append(r)
                    continue
                l = range(r.start, rng.start)
                r = range(rng.stop, r.stop)
                if len(l) > 0:
                    new_rng.append(l)
                if len(r) > 0:
                    new_rng.append(r)
            return ranges(new_rng)

        raise TypeError('invalid arguments')

    def count(self, value: int) -> int:
        for r in self._ranges:
            if r.count(value) == 1:
                return 1
        return 0

    def index(self, value: int) -> int:
        acc = 0
        for r in self._ranges:
            if value in r:
                return acc + r.index(value)
            acc += len(r)
        raise ValueError(f'{value} is not in ranges')

    @overload
    def __or__(self, other: "ranges") -> "ranges": ...
    @overload
    def __or__(self, other: range) -> "ranges": ...

    def __or__(self, other) -> "ranges":
        return self.union(other)

    @overload
    def __and__(self, other: "ranges") -> "ranges": ...
    @overload
    def __and__(self, other: range) -> "ranges": ...

    def __and__(self, other) -> "ranges":
        return self.intersection(other)

    @overload
    def __sub__(self, other: "ranges") -> "ranges": ...
    @overload
    def __sub__(self, other: range) -> "ranges": ...

    def __sub__(self, other) -> "ranges":
        return self.difference(other)

    def __len__(self) -> int:
        return sum((len(r) for r in self._ranges))

    def __contains__(self, o: object) -> bool:
        return any(map(lambda r: o in r, self._ranges))

    def __iter__(self) -> Iterator[int]:
        return itertools.chain(*self._ranges)

    @overload
    def __getitem__(self, i: int) -> int: ...
    @overload
    def __getitem__(self, s: slice) -> range: ...

    def __getitem__(self, first):
        if isinstance(first, int):
            i = first
            acc = 0
            if i >= 0:
                for r in self._ranges:
                    if acc + len(r) > i:
                        return r[i - acc]
                    acc += len(r)
            else:
                for r in reversed(self._ranges):
                    if acc - len(r) <= i:
                        return r[i - acc]
                    acc -= len(r)
            raise IndexError('ranges object index out of range')

        if isinstance(first, slice):
            s = first
            start, stop, stride = s.indices(len(self))
            result = []
            # TODO: this can be more efficient
            for i in range(start, stop, stride):
                result.append(self[i])
            return result

        raise TypeError('invalid arguments')

    def __repr__(self) -> str:
        ranges_str = ', '.join((f'[{r.start}, {r.stop})' for r in self._ranges))
        return f'ranges({ranges_str})'

    def __reversed__(self) -> Iterator[int]:
        return itertools.chain(*map(reversed, reversed(self._ranges)))

def range_intersection(r1: range, r2: range) -> ranges:
    return ranges(r1).intersection(r2)

def range_union(r1: range, r2: range) -> ranges:
    return ranges(r1).union(r2)

def range_diffrence(r1: range, r2: range) -> ranges:
    return ranges(r1).difference(r2)

def range_intersects(r1: range, r2: range) -> bool:
    return len(range_intersection(r1, r2)) > 0
