import os
import sys
import heapq
import math
import time

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.n = len(init_state)
        # self.actions = list() - Don't really need this.

    def solve(self):
        #TODO
        # implement your search algorithm here
        # Get unmodifiable states
        start_time = time.time()
        print('Solving...')
        unmodifiable_initial_state = tuple(tuple(i) for i in self.init_state)
        unmodifiable_goal_state = tuple(tuple(i) for i in self.goal_state)
        # Exit if not solvable
        if not self.__is_solvable(unmodifiable_initial_state):
            return ["UNSOLVABLE"]
        start_node = Node(unmodifiable_initial_state, 0, False, False)
        frontier = []
        heapq.heapify(frontier)
        heapq.heappush(frontier, (0, start_node))
        visited = {}
        goal_found = False
        goal_node = False
        while len(frontier) > 0 and not goal_found:
            current = heapq.heappop(frontier)
            if (current[1].state in visited):
                continue
            else:
                visited[current[1].state] = 1
            
            if (current[1].has_state_equals_to(unmodifiable_goal_state)):
                goal_found = True
                goal_node = current[1]
                break
            successors = current[1].get_successors()
            # Successors are a list of Nodes.
            for successor in successors:
                if successor.state not in visited:
                    fn = successor.get_actual_cost() + 1.0001*successor.get_heuristic_cost()
                    heapq.heappush(frontier, (fn, successor))
        path = self.__get_path(unmodifiable_initial_state, goal_node)
        print(self.__apply_moves_on_state(unmodifiable_initial_state, path))
        print('Execution time: {duration}'.format(duration=(time.time() - start_time)))
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
            for i in range (0, self.n):
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
            for j in range (0, self.n):
                if not initial_state[i][j] == 0:
                    one_dimensional_list.append(initial_state[i][j])
                else:
                    row_where_zero_is = i
        for i in range(0, len(one_dimensional_list)):
            for j in range (i, len(one_dimensional_list)):
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
    def __get_path(self, init_state, goal_node):
        path = []
        def recursive_backtrack(node):
            if not node.has_state_equals_to(init_state):
                recursive_backtrack(node.parent)
                path.append(node.direction)
        recursive_backtrack(goal_node)
        return path

class Node(object):
    def __init__(self, state, g, parent, direction):
        self.state = state
        self.g = g
        self.n = len(state)
        self.parent = parent
        self.direction = direction
    
    def __lt__(self, other):
        return self.g < other.g

    def has_state_equals_to(self, other_state):
        is_equals = True
        for i in range (0, self.n):
            for j in range (0, self.n):
                if self.state[i][j] != other_state[i][j]:
                    is_equals = False
                    break
        return is_equals

    def get_heuristic_cost(self):
        # Implement the heuristics. Try Manhatten distance with linear conflict.
        return self.__get_manhatten() + 2 * self.__get_linear_conflict()
    
    def __get_manhatten(self):
        distance = 0
        for i in range (0, self.n):
            for j in range(0, self.n):
                value = self.state[i][j]
                if value != 0:
                    correct_index = [math.floor((value - 1)/self.n), (value - 1) % self.n]
                    distance += abs(correct_index[0] - i) + abs(correct_index[1] - j)
                else:
                    distance += (self.n - i - 1) + (self.n - j - 1)
        return distance

    def __get_linear_conflict(self):
        linear_conflict = 0
        # Count linear conflicts
        for i in range(0, self.n):
            for j in range(0, self.n):
                value = self.state[i][j]
                # If value is in the correct row.
                if value != 0 and (value - 1)//self.n == i:
                    for k in range(j + 1, self.n):
                        if self.state[i][k] != 0 and (self.state[i][k] - 1)//self.n == i and value > self.state[i][k]:
                            linear_conflict += 1
                            #print('conflict at {v1}, {v2}'.format(v1 = value, v2 = self.state[i][k]))
                # If value is in the correct col.
                if value != 0 and (value - 1)%self.n == j:
                    for k in range(i + 1, self.n):
                        if self.state[k][j] != 0 and (self.state[k][j] - 1)%self.n == j and value > self.state[k][j]:
                            linear_conflict += 1
                            #print('conflict at {v1}, {v2}'.format(v1 = value, v2 = self.state[k][j]))
        '''print(self.state)
        print('has linear conflict: {value}'.format(value=linear_conflict))
        print('\n')'''
        return linear_conflict

    def is_opposite_direction(self, direction1, direction2):
        opposite_directions = { "LEFT": "RIGHT",
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
        for i in range (0, self.n):
            for j in range (0, self.n):
                if self.state[i][j] == 0:
                    zero_row = i
                    zero_col = j
                    break
        
        # Obtain next set of states.
        up_index = [zero_row - 1, zero_col, "DOWN"]
        left_index = [zero_row, zero_col - 1, "RIGHT"]
        right_index = [zero_row, zero_col + 1, "LEFT"]
        down_index = [zero_row + 1, zero_col, "UP"]
        indices = [up_index, left_index, right_index, down_index]
        for index in indices:
            # Ignore if indices out of bound.
            if (index[0] < 0 or index[0] >= self.n) or (index[1] < 0 or index[1] >= self.n):
                continue
            # Don't go back to previous state (opposite direction).
            if self.is_opposite_direction(self.direction, index[2]):
                continue
            next_state = [list(i) for i in self.state]
            next_state[zero_row][zero_col] = next_state[index[0]][index[1]]
            next_state[index[0]][index[1]] = 0
            successors.append(Node(tuple(tuple(i) for i in next_state), self.g + 1, self, index[2]))
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
    

    i,j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number , base = 10)
            if  0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')

