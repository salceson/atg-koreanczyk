from koreanczyk.utils.helpers import *


def test_forward__from_outside():
    assert forward(-1, 1) == 1
    assert forward(-1, 2) == 2
    assert forward(-1, 3) == 3
    assert forward(-1, 4) == 4
    assert forward(-1, 5) == 5


def test_forward_rectangle_path():
    for i in range(20):
        assert forward(i, 1) == i + 1 if i + 1 < 20 else 100
        assert forward(i, 2) == i + 2 if i + 2 < 20 else 100
        assert forward(i, 3) == i + 3 if i + 3 < 20 else 100
        assert forward(i, 4) == i + 4 if i + 4 < 20 else 100
        assert forward(i, 5) == i + 5 if i + 5 < 20 else 100

    for i in range(20, 36):
        assert forward(i, 1) == i + 1 if i + 1 < 36 else 100
        assert forward(i, 2) == i + 2 if i + 2 < 36 else 100
        assert forward(i, 3) == i + 3 if i + 3 < 36 else 100
        assert forward(i, 4) == i + 4 if i + 4 < 36 else 100
        assert forward(i, 5) == i + 5 if i + 5 < 36 else 100

    for i in range(40, 56):
        assert forward(i, 1) == i + 1 if i + 1 < 56 else 100
        assert forward(i, 2) == i + 2 if i + 2 < 56 else 100
        assert forward(i, 3) == i + 3 if i + 3 < 56 else 100
        assert forward(i, 4) == i + 4 if i + 4 < 56 else 100
        assert forward(i, 5) == i + 5 if i + 5 < 56 else 100

    for i in range(60, 71):
        assert forward(i, 1) == i + 1 if i + 1 < 71 else 100
        assert forward(i, 2) == i + 2 if i + 2 < 71 else 100
        assert forward(i, 3) == i + 3 if i + 3 < 71 else 100
        assert forward(i, 4) == i + 4 if i + 4 < 71 else 100
        assert forward(i, 5) == i + 5 if i + 5 < 71 else 100


def test_turning_left():
    assert turn_left(5, 1) == 26
    assert turn_left(5, 2) == 27
    assert turn_left(5, 3) == 28
    assert turn_left(5, 4) == 29
    assert turn_left(5, 5) == 30

    assert turn_left(10, 1) == 51
    assert turn_left(10, 2) == 52
    assert turn_left(10, 3) == 53
    assert turn_left(10, 4) == 54
    assert turn_left(10, 5) == 55

    assert turn_left(28, 1) == 69
    assert turn_left(28, 2) == 70
    assert turn_left(28, 3) == 100
    assert turn_left(28, 4) == 100
    assert turn_left(28, 5) == 100


def test_forward_left_down_diagonal():
    result_positions = [26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
    for current in [26, 27, 28, 29, 30]:
        for x in range(1, 6):
            assert forward(current, x) == result_positions[result_positions.index(current) + x]


def test_forward_left_up_diagonal():
    result_positions = [51, 52, 53, 54, 55, 100, 100, 100, 100, 100]
    for current in [51, 52, 53, 54, 55]:
        for x in range(1, 6):
            assert forward(current, x) == result_positions[result_positions.index(current) + x]


def test_backward():
    special = [26, 51, 69]
    special_results = [5, 10, 28]
    for i, s in enumerate(special):
        assert backward(s) == special_results[i]

    # 'ez' backward win
    assert backward(1) == 100
    assert backward(21) == 100
    assert backward(41) == 100
    assert backward(61) == 100

    ###
    current = 32
    current = backward(current)
    assert current == 31
    current = backward(current)
    assert current == 30
    current = forward(current, 1)
    assert current == 31

    ###
    current = 69
    current = backward(current)
    assert current == 28
    current = backward(current)
    assert current == 27
    current = forward(current, 1)
    assert current == 28
    current = forward(current, 1)
    assert current == 29

    ###
    current = 51
    current = backward(current)
    assert current == 10
    current = backward(current)
    assert current == 9
    current = forward(current, 1)
    assert current == 10
    current = forward(current, 1)
    assert current == 11


if __name__ == '__main__':
    test_forward__from_outside()
    test_forward_rectangle_path()
    test_turning_left()
    test_forward_left_down_diagonal()
    test_forward_left_up_diagonal()
    test_backward()
