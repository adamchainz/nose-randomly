def _test_func(arg):
    pass


def test_generator():
    yield _test_func, 'A'
    yield _test_func, 'B'
    yield _test_func, 'C'
    yield _test_func, 'D'
