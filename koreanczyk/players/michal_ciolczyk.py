import random

from koreanczyk.utils.commands import Move
from koreanczyk.utils.helpers import forward, backward, turn_left


class Player(object):
    def __init__(self):
        super(Player, self).__init__()
        self.i = -1

    def name(self, i):
        self.i = i

    def board(self, i, player_structs):
        self.my_state = player_structs[self.i]

    def paticks(self, i):
        """Output format, e.g.: ['X', 'O']"""
        if i != self.i:  # Opponent's move
            return ['X', 'O']
        else:  # My move
            return ['O', 'O']

    def throw_result(self, i, s):
        if s in ['yut', 'mo']:
            # throwing again
            pass

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

    def _max_counter_group(self):
        not_finished_counter_groups = self._not_finished_counter_groups()
        if len(not_finished_counter_groups) > 0:
            return max(not_finished_counter_groups.keys(), key=lambda k: not_finished_counter_groups[k])
        else:
            return random.choice(self.my_state.state.keys())

    def _min_counter_group(self):
        counter_groups_after_start = self._counter_groups_after_start()
        if len(counter_groups_after_start) > 0:
            return min(counter_groups_after_start.keys(), key=lambda k: counter_groups_after_start[k])
        else:
            return random.choice(self.my_state.state.keys())

    def _is_possible_to_turn(self, current):
        return current in [5, 10, 28]
