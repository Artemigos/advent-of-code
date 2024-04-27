import traceback
from . import neighbors_ortho

def test(f, *tests):
    results = []
    for t in tests:
        try:
            t()
            results.append((t, 'ok'))
        except:
            results.append((t, 'fail'))
            print(f.__name__, t.__name__, 'failure:')
            print(traceback.format_exc())
    print()
    for t, r in results:
        print(f.__name__, t.__name__, ':', r)

def two_dimensions():
    n2d = list(neighbors_ortho((1, 11)))
    assert (0, 11) in n2d
    assert (2, 11) in n2d
    assert (1, 10) in n2d
    assert (1, 12) in n2d

    assert (0, 10) not in n2d
    assert (0, 12) not in n2d
    assert (2, 10) not in n2d
    assert (2, 12) not in n2d
    assert (1, 11) not in n2d

def three_dimensions():
    n3d = list(neighbors_ortho((1, 11, 101)))
    assert (0, 11, 101) in n3d
    assert (2, 11, 101) in n3d
    assert (1, 10, 101) in n3d
    assert (1, 12, 101) in n3d
    assert (1, 11, 100) in n3d
    assert (1, 11, 102) in n3d

    assert (0, 10, 100) not in n3d
    assert (1, 10, 100) not in n3d
    assert (2, 10, 100) not in n3d
    assert (0, 11, 100) not in n3d
    assert (2, 11, 100) not in n3d
    assert (0, 12, 100) not in n3d
    assert (1, 12, 100) not in n3d
    assert (2, 12, 100) not in n3d
    assert (0, 10, 102) not in n3d
    assert (1, 10, 102) not in n3d
    assert (2, 10, 102) not in n3d
    assert (0, 11, 102) not in n3d
    assert (2, 11, 102) not in n3d
    assert (0, 12, 102) not in n3d
    assert (1, 12, 102) not in n3d
    assert (2, 12, 102) not in n3d
    assert (0, 10, 101) not in n3d
    assert (2, 10, 101) not in n3d
    assert (0, 12, 101) not in n3d
    assert (2, 12, 101) not in n3d
    assert (1, 11, 101) not in n3d

test(neighbors_ortho, two_dimensions, three_dimensions)
