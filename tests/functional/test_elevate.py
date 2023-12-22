from functional.monadic import elevate


def test_elevate():
    assert elevate(lambda x: x + 1, 1) is not None
