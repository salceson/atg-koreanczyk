import random

from koreanczyk.utils.commands import Move
from koreanczyk.utils.helpers import forward, backward, turn_left

_MY_DEFAULT_PATICKS = ['OO', 'XX']
_OPPONENT_DEFAULT_PATICKS = ['XO']
_OPPONENT_THROW_FOR_RESULT = {
    'do': {
        'XX': 'XO',
        'XO': 'XX'
    },
    'gae': {
        'XX': 'OO',
        'OO': 'XX',
        'XO': 'XO'
    },
    'geol': {
        'OO': 'XO',
        'XO': 'OO'
    },
    'yut': {
        'OO': 'OO'
    },
    'mo': {
        'XX': 'XX'
    }
}
_BEST_RESPONSES_MY = {
    'XX': ['XX'],
    'OO': ['OO'],
    'XO': ['OO', 'XO']
}
_BEST_RESPONSES_OPPONENT = {
    'XX': ['XO'],
    'XO': ['XX'],
    'OO': ['XX']
}


class Player(object):
    def __init__(self):
        super(Player, self).__init__()
        self.i = 0
        self.previous_rethrow = False
        self.consecutive_rethrows = 0
        self.opponents_moves = {0: 'XX', 1: 'XO'}
        self.my_paticks = 'OO'
        self.my_moves = {0: 'XO', 1: 'OO'}

    def name(self, i):
        self.i = i
        self.my_moves[i] = _MY_DEFAULT_PATICKS
        self.my_moves[1 - i] = _OPPONENT_DEFAULT_PATICKS
        self.opponents_moves[i] = 'XO'
        self.opponents_moves[1 - i] = 'OO'
        self.consecutive_rethrows = 0

    def board(self, i, player_structs):
        self.my_state = player_structs[self.i]

    def paticks(self, i):
        """Output format, e.g.: ['X', 'O']"""
        self.my_paticks = random.choice(self.my_moves[i])
        return [self.my_paticks[0], self.my_paticks[1]]

    def throw_result(self, i, s):
        opponent_throw = _OPPONENT_THROW_FOR_RESULT[s][self.my_paticks]
        self.opponents_moves[i] = opponent_throw
        best_responses = _BEST_RESPONSES_MY if self.i == i else _BEST_RESPONSES_OPPONENT
        self.my_moves[i] = best_responses[opponent_throw]
        is_rethrow = s in ['yut', 'mo']
        self.consecutive_rethrows = self.consecutive_rethrows + 1 if is_rethrow else 0
        if self.consecutive_rethrows > 1000 and self.i == i and is_rethrow:
            if s is 'yut':
                self.my_moves[i] = ['XO']
            else:
                self.my_moves[i] = ['OO']

    def moves(self, i, moves_list):
        """Input format: [1, 3, -1],
        Output format, e.g.: [Move(CounterGroup(1),'forward', 3), Move(CounterGroup(2, 3), 'turn_left', 5), Merge(CounterGroup(1), CounterGroup(2))] """
        if i == self.i:
            output = []
            for move in sorted(moves_list, reverse=True):
                if move == -1:
                    choice_group = self._min_counter_group()
                    self.my_state.state[choice_group] = backward(self.my_state.state[choice_group])
                    output.append(Move(choice_group, 'forward', move))
                else:
                    choice_group = self._possible_to_turn_group(move)
                    if not choice_group:
                        choice_group = self._max_counter_group()
                    current = self.my_state.state[choice_group]
                    if self._is_possible_to_turn(current):
                        moved = turn_left(current, move)
                        my_move = 'turn_left'
                    else:
                        moved = forward(current, move)
                        my_move = 'forward'
                    self.my_state.state[choice_group] = moved
                    output.append(Move(choice_group, my_move, move))
            return output

    def end(self, i):
        pass

    def _not_finished_counter_groups(self):
        return {key: value for key, value in self.my_state.state.iteritems() if value != 100}

    def _counter_groups_after_start(self):
        return {key: value for key, value in self.my_state.state.iteritems() if value != -1}

    def _distance_to_end(self, pos):
        if pos < 0:
            return 20
        if 0 <= pos < 20:
            return 20 - pos
        if 20 <= pos < 36:
            return 36 - pos
        if 40 <= pos < 56:
            return 56 - pos
        if 60 <= pos < 71:
            return 71 - pos
        return 100

    def _max_counter_group(self):
        not_finished_counter_groups = self._not_finished_counter_groups()
        if len(not_finished_counter_groups) > 0:
            return max(not_finished_counter_groups.keys(),
                       key=lambda k: self._distance_to_end(not_finished_counter_groups[k]))
        else:
            return random.choice(self.my_state.state.keys())

    def _min_counter_group(self):
        counter_groups_after_start = self._counter_groups_after_start()
        if len(counter_groups_after_start) > 0:
            return min(counter_groups_after_start.keys(),
                       key=lambda k: self._distance_to_end(counter_groups_after_start[k]))
        else:
            return random.choice(self.my_state.state.keys())

    def _is_possible_to_turn(self, current):
        return current in [5, 10, 28]

    def _possible_to_turn_group(self, move):
        for key, value in self.my_state.state.iteritems():
            if self._is_possible_to_turn(value + move):
                return key
        return None
