# I
#########################
#  10   9   8   7   6   5
#  11                   4
#  12                   3
#
#  13                   2
#  14                   1
#  15  16  17  18  19   0
#########################

# II
#########################
#                      25
#                  26  24
#               27     23
#            28
#         29           22
#      30              21
#  31  32  33  34  35  20
#########################

# III
#########################
#  50  49  48  47  46  45
#      51              44
#         52           43
#            53
#               54     42
#                  55  41
#                      40
#########################

# IV
#########################
#                      65
#                  66  64
#               67     63
#            68
#               69     62
#                  70  61
#                      60
#########################

same_places = [[0, 20, 40, 60],
               [1, 21, 41, 61],
               [2, 22, 42, 62],
               [3, 23, 43, 63],
               [4, 24, 44, 64],
               [5, 25, 45, 65],
               [6, 46],
               [7, 47],
               [8, 48],
               [9, 49],
               [10, 50],
               [11],
               [12],
               [13],
               [14],
               [15, 31],
               [16, 32],
               [17, 33],
               [18, 34],
               [19, 35],
               [26, 66],
               [27, 67],
               [28, 53, 68],
               [29],
               [30],
               [51],
               [52],
               [54, 69],
               [55, 70]]


def same_place(a, b):
    for same_place_list in same_places:
        if a in same_place_list and b in same_place_list:
            return True
    return False


def get_moves_list(current):
    if 0 <= current < 20:
        return range(20)
    if 20 <= current < 36:
        return range(20, 36)
    if 40 <= current < 56:
        return range(40, 56)
    if 60 <= current < 71:
        return range(60, 71)


def forward(current, i):
    if i == -1:  # todo test for forward(current, -1) -> backward
        return backward(current)
    if current == -1:
        return forward(0, i)
    if current == 100:
        return 100
    _list = get_moves_list(current)
    try:
        place = _list[_list.index(current) + i]
    except IndexError:
        return 100
    return place


def backward(current):
    # if crossroads backward -> choose longer/default path
    if current == 26:
        return 5
    if current == 51:
        return 10
    if current == 69:
        return 28
    if current == 100:
        return 100
    _list = get_moves_list(current)
    current_idx = _list.index(current)
    if current_idx == 1:
        return 100
    else:
        return _list[current_idx - 1]


def turn_left(current, i):
    if current == 5:
        return forward(current + 20, i)
    elif current == 10:
        return forward(current + 40, i)
    elif current == 28:
        return forward(current + 40, i)
    else:
        raise ValueError("Current place is not on the crossroad")
