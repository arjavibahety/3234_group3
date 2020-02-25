import os
import sys
import heapq
import time


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.n = len(init_state)
        # self.actions = list() - Don't really need this.

    def solve(self):
        # TODO
        # implement your search algorithm here
        # Get unmodifiable states
        start_time = time.time()
        print('Solving...')
        unmodifiable_initial_state = tuple(tuple(i) for i in self.init_state)
        unmodifiable_goal_state = tuple(tuple(i) for i in self.goal_state)

        # Exit if not solvable
        if not self.__is_solvable(unmodifiable_initial_state):
            return ["UNSOLVABLE"]
        start_node = Node(unmodifiable_initial_state, 0,
                          False, False)
        frontier = []  # Bucket()
        # frontier.push(start_node)
        heapq.heapify(frontier)
        heapq.heappush(frontier, start_node)
        visited = {unmodifiable_initial_state: start_node}
        goal_found = False
        goal_node = False
        while len(frontier) > 0 and not goal_found:
            current = heapq.heappop(frontier)
            #current = frontier.pop()
            if (current.has_state_equals_to(unmodifiable_goal_state)):
                goal_found = True
                goal_node = current
                break
            successors = current.get_successors()
            # Successors are a list of Nodes.
            for successor in successors:
                if successor.state not in visited or successor.g < visited[successor.state].g:
                    visited[successor.state] = successor
                    heapq.heappush(frontier, successor)
                    # frontier.push(successor)
        path = self.__get_path(goal_node.state, visited)
        #print('Testing path produced. Path brings the initial state to: {final_state}'.format(final_state=self.__apply_moves_on_state(unmodifiable_initial_state, path)))
        print('Execution time: {duration}'.format(
            duration=(time.time() - start_time)))
        return path

    # Function to test if algorithm produces the correct goal state.
    # Input is a list of moves e.g ["UP", "DOWN", "LEFT"], returns the state
    # After executing all the moves on the initial_state.
    def __apply_moves_on_state(self, initial_state, moves):
        if len(moves) == 0:
            return initial_state
        else:
            zero_row = -1
            zero_col = -1
            for i in range(0, self.n):
                for j in range(0, self.n):
                    if initial_state[i][j] == 0:
                        zero_row = i
                        zero_col = j
                        break
            modifiable_state = [list(k) for k in initial_state]
            move = moves[0]
            if move == "LEFT":
                modifiable_state[zero_row][zero_col] = modifiable_state[zero_row][zero_col + 1]
                modifiable_state[zero_row][zero_col + 1] = 0
            elif move == "RIGHT":
                modifiable_state[zero_row][zero_col] = modifiable_state[zero_row][zero_col - 1]
                modifiable_state[zero_row][zero_col - 1] = 0
            elif move == "DOWN":
                modifiable_state[zero_row][zero_col] = modifiable_state[zero_row - 1][zero_col]
                modifiable_state[zero_row - 1][zero_col] = 0
            else:
                modifiable_state[zero_row][zero_col] = modifiable_state[zero_row + 1][zero_col]
                modifiable_state[zero_row + 1][zero_col] = 0
            next_state = tuple(tuple(k) for k in modifiable_state)
            return self.__apply_moves_on_state(next_state, moves[1::])

    # Function to check if the puzzle is solvable
    def __is_solvable(self, initial_state):
        inversions = 0
        one_dimensional_list = []
        row_where_zero_is = -1
        for i in range(0, self.n):
            for j in range(0, self.n):
                if not initial_state[i][j] == 0:
                    one_dimensional_list.append(initial_state[i][j])
                else:
                    row_where_zero_is = i
        for i in range(0, len(one_dimensional_list)):
            for j in range(i, len(one_dimensional_list)):
                if one_dimensional_list[i] > one_dimensional_list[j]:
                    inversions += 1

        # If n is odd, the puzzle is solvable if the number of inversions is even.
        # Otherwise, the puzzle is solvable if
        # 1) The number of inversions is odd and the row index of 0 is even.
        # 2) The number of inversions is even and the row index of 0 is odd.
        if len(initial_state) % 2 == 1:
            return inversions % 2 == 0
        else:
            return (inversions % 2 == 0 and row_where_zero_is % 2 == 1) or (inversions % 2 == 1 and row_where_zero_is % 2 == 0)

    # you may add more functions if you think is useful
    def __get_path(self, goal_state, dictionary):
        path = []

        def recursive_backtrack(state):
            node = dictionary[state]
            if node.has_parent():
                recursive_backtrack(node.parent.state)
                path.append(node.direction)
        recursive_backtrack(goal_state)
        return path


class Node(object):
    def __init__(self, state, g, parent, direction):
        self.state = state
        self.g = g
        self.n = len(state)
        self.parent = parent
        self.direction = direction
        self.f = self.g + self.__get_heuristic_cost()

    def __lt__(self, other):
        # return self.g > other.g
        if self.f < other.f or self.f > other.f:
            return self.f < other.f
        else:
            return self.g > other.g

    def has_parent(self):
        return self.parent != False

    def has_state_equals_to(self, other_state):
        is_equals = True
        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.state[i][j] != other_state[i][j]:
                    is_equals = False
                    break
        return is_equals

    def __get_heuristic_cost(self):
        return self.__get_manhatten()

    def __get_manhatten(self):
        manhattan_dis = 0
        state = self.state

        for i in range(0, len(state)):
            for j in range(0, len(state)):
                value = state[i][j]
                if state[i][j] != 0:
                    goal_coords = [(value - 1)//self.n, (value - 1) % self.n]
                    manhattan_dis += abs(goal_coords[0] - i) + \
                        abs(goal_coords[1] - j)

        return manhattan_dis

    def is_opposite_direction(self, direction1, direction2):
        opposite_directions = {"LEFT": "RIGHT",
                               "RIGHT": "LEFT",
                               "UP": "DOWN",
                               "DOWN": "UP"}
        return direction1 == opposite_directions[direction2]

    def get_actual_cost(self):
        return self.g

    def get_successors(self):
        successors = []
        zero_row = -1
        zero_col = -1
        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.state[i][j] == 0:
                    zero_row = i
                    zero_col = j
                    break

        # Obtain next set of states.
        up_index = {"row": zero_row - 1, "col": zero_col, "direction": "DOWN"}
        left_index = {"row": zero_row,
                      "col": zero_col - 1, "direction": "RIGHT"}
        right_index = {"row": zero_row,
                       "col": zero_col + 1, "direction": "LEFT"}
        down_index = {"row": zero_row + 1, "col": zero_col, "direction": "UP"}
        indices = [up_index, left_index, right_index, down_index]
        for index in indices:
            # Ignore if indices out of bound.
            if (index["row"] < 0 or index["row"] >= self.n) or (index["col"] < 0 or index["col"] >= self.n):
                continue
            # Don't go back to previous state (opposite direction).
            if self.is_opposite_direction(self.direction, index["direction"]):
                continue
            next_state = [list(i) for i in self.state]
            next_state[zero_row][zero_col] = next_state[index["row"]
                                                        ][index["col"]]
            next_state[index["row"]][index["col"]] = 0
            successors.append(
                Node(tuple(tuple(i) for i in next_state), self.g + 1, self, index["direction"]))
        return successors


if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()

    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]

    i, j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number, base=10)
            if 0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1) % n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')
