"""
Rush hour in python
"""

import sys


class Move(object):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    tostr = {
        UP: 'UP',
        DOWN: 'DOWN',
        LEFT: 'LEFT',
        RIGHT: 'RIGHT'
    }


class Board(object):
    def __init__(self, table, move=None, parent=None, coordinate=None):
        self.table = table
        self.parent = parent
        self.move = move
        self.coordinate = coordinate
        self.children = []

    def add_child(self, board):
        self.children.append(board)

    def has_same_table_as(self, board):
        return self.table == board.table


def print_path(board, show_board=False, horizontal=False):
    boards = []
    while board.parent is not None:
        boards.append(board)
        board = board.parent

    size = len(board.table)
    for cur_board in reversed(boards):
        cur_type = cur_board.table[cur_board.coordinate[0]][cur_board.coordinate[1]]
        print("%s-%s" % (cur_type, Move.tostr[cur_board.move].title()))
        if show_board and not horizontal:
            print("\n".join(" ".join(row) for row in cur_board.table))

    if show_board and horizontal:
        for i, row in enumerate(range(size)):
            print(("  =>  " if size / 2 == i else "      ").join([" ".join(cur_board.table[row]) for cur_board in reversed(boards)]))


def solve(board, size, goal_car):

    goal_car_start = None
    goal_car_end = None
    goal_row = None
    for row_index, row in enumerate(board.table):
        try:
            rowstr = "".join(row)
            goal_car_start = rowstr.index(goal_car)
            goal_car_end = rowstr.rindex(goal_car)
            goal_row = row_index
        except ValueError:
            continue

    if goal_row is None or goal_car_end is None or goal_car_start is None:
        print("Could not find goal state")
        return False

    boards = [board]
    idx = 0
    while True:
        cur_board = boards[idx]
        if cur_board.table[goal_row][size - 1] == cur_board.table[goal_row][size - 1 - (goal_car_end - goal_car_start)] == goal_car:
            print_path(cur_board)
            return True

        continue_with_next_board = False
        for i in range(idx):
            if cur_board.has_same_table_as(boards[i]):
                continue_with_next_board = True
                break

        if continue_with_next_board:
            idx += 1
            continue

        for directional_move_fn in [gen_horizontal_moves, gen_vertical_moves]:
            for (m, coordinate) in directional_move_fn(cur_board.table, size):
                new_board_table = make_new_board_from_move(cur_board.table, size, m, coordinate)
                new_board = Board(new_board_table, m, cur_board, coordinate)
                cur_board.add_child(new_board)
                boards.append(new_board)

        idx += 1


def parse_board(str_board):
    return [list(line) for line in str_board.strip().splitlines()]


def print_board_obj(board_obj):
    print('\n'.join(''.join(row) for row in board_obj))


def make_new_board_from_move(board_obj, size, move, coordinate):
    new_board_obj = [row[:] for row in board_obj]
    if move == Move.LEFT:
        row, col = coordinate
        car_type = new_board_obj[row][col + 1]
        for i in range(col + 1, size):
            if new_board_obj[row][i] != car_type:
                new_board_obj[row][i - 1], new_board_obj[row][col] = new_board_obj[row][col], new_board_obj[row][i - 1]
                break
            elif i == size - 1:
                new_board_obj[row][i], new_board_obj[row][col] = new_board_obj[row][col], new_board_obj[row][i]
                break
        return new_board_obj
    elif move == Move.RIGHT:
        row, col = coordinate
        car_type = new_board_obj[row][col - 1]
        for i in range(col - 1, -1, -1):
            if new_board_obj[row][i] != car_type:
                new_board_obj[row][i + 1], new_board_obj[row][col] = new_board_obj[row][col], new_board_obj[row][i + 1]
                break
            elif i == 0:
                new_board_obj[row][i], new_board_obj[row][col] = new_board_obj[row][col], new_board_obj[row][i]
                break
        return new_board_obj

    elif move == Move.UP:
        row, col = coordinate
        car_type = new_board_obj[row + 1][col]
        for i in range(row + 1, size):
            if new_board_obj[i][col] != car_type:
                new_board_obj[i - 1][col], new_board_obj[row][col] = new_board_obj[row][col], new_board_obj[i - 1][col]
                break
            elif i == size - 1:
                new_board_obj[i][col], new_board_obj[row][col] = new_board_obj[row][col], new_board_obj[i][col]
                break
        return new_board_obj

    elif move == Move.DOWN:
        row, col = coordinate
        car_type = new_board_obj[row - 1][col]
        for i in range(row - 1, -1, -1):
            if new_board_obj[i][col] != car_type:
                new_board_obj[i + 1][col], new_board_obj[row][col] = new_board_obj[row][col], new_board_obj[i + 1][col]
                break
            elif i == 0:
                new_board_obj[i][col], new_board_obj[row][col] = new_board_obj[row][col], new_board_obj[i][col]
                break
        return new_board_obj

    return board_obj


def gen_horizontal_moves(board_obj, board_length):
    for i, row in enumerate(board_obj):
        for move, blank_index in gen_moves_in_line(row, board_length):
            yield (move, (i, blank_index))


def gen_vertical_moves(board_obj, board_length):
    for i in range(board_length):
        col = [row[i] for row in board_obj]
        for move, blank_index in gen_moves_in_line(col, board_length):
            yield (Move.UP if move == Move.LEFT else Move.DOWN, (blank_index, i))


def gen_moves_in_line(line, length):
    blank_char = '.'
    blank_indices = [bi for bi, blank in enumerate(line) if blank == blank_char]
    if not blank_indices:
        return
    for blank_index in blank_indices:
        right1 = blank_index + 1
        right2 = blank_index + 2
        if right2 < length and line[right1] == line[right2] and line[right1] != blank_char:
            yield (Move.LEFT, blank_index)

        left1 = blank_index - 1
        left2 = blank_index - 2
        if left2 >= 0 and line[left1] == line[left2] and line[left1] != blank_char:
            yield (Move.RIGHT, blank_index)


def main():
    initialboard = parse_board(sys.stdin.read())
    board = Board(initialboard, None, None)
    solve(board, len(initialboard), "r")


if __name__ == '__main__':
    main()
