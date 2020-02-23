import os
import sys
import heapq
import time


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()

    def solve(self):
        # TODO
        # implement your search algorithm here

        start_time = time.time()
        if not self.is_solvable(init_state):
            return ["UNSOLVABLE"]

        goal_state_hash = self.get_goal_state_hash(goal_state)
        goal_state_tuple = tuple(tuple(i) for i in goal_state)

        start_node = Node(tuple(tuple(i) for i in init_state),
                          0, False, False, goal_state_hash)

        # frontier = []
        frontier = Bucket()
        frontier.push(start_node)
        visited = {}
        # heapq.heapify(frontier)
        # heapq.heappush(frontier, start_node)
        goal_node = False
        is_goal_not_found = True
        current = True

        # while len(frontier) > 0:
        while frontier.n > 0 and current and is_goal_not_found:
            # current = heapq.heappop(frontier)
            current = frontier.pop()
            if visited.get(current.state) and visited[current.state].g < current.g:
                continue

            visited[current.state] = current

            if self.is_equal_states(current.state, goal_state_tuple):
                goal_node = current
                is_goal_not_found = False
                break

            neighbors = current.get_neighbors()

            for neighbor in neighbors:
                if visited.get(neighbor.state) and visited[neighbor.state].g <= neighbor.g:
                    continue

                frontier.push(neighbor)

        path = self.get_path(goal_node.state, visited)

        print("Goal Node State: ", goal_node.state)
        print('Time taken: {duration}'.format(
            duration=(time.time() - start_time)))

        return path  # sample output

    # you may add more functions if you think is useful
    def is_solvable(self, init_state):
        inversions = 0
        n = len(init_state)
        condensed = []
        row_of_zero = -1

        for i in range(0, n):
            for j in range(0, n):
                condensed.append(init_state[i][j])
                if init_state[i][j] == 0:
                    row_of_zero = i

        # Calculate number of inversions
        for i in range(0, len(condensed)):
            for j in range(0, i):
                if condensed[i] < condensed[j] and condensed[i] != 0 and condensed[j] != 0:
                    inversions += 1

        # If board size is odd & inversions is even --> solvable
        if n % 2 == 1:
            return inversions % 2 == 0

        # If board size if even, inversions + row of 0 is odd --> solvable
        return (inversions + row_of_zero) % 2 == 1

    # Store the final coordinates of the goal state in a hashtable
    def get_goal_state_hash(self, goal_state):
        goal_state_hash = {}

        for i in range(0, len(goal_state)):
            for j in range(0, len(goal_state)):
                goal_state_hash[goal_state[i][j]] = (i, j)

        return goal_state_hash

    def is_equal_states(self, s1, s2):
        return s1 == s2

    def get_path(self, goal_state, visited):
        path = []
        # print("Printing Path: ")

        def helper(state):
            # get the current node of the current state
            current = visited[state]
            if current.parent:
                helper(current.parent.state)
                path.append(current.direction)
                # print("F: ", current.f, " G: ", current.g)

        helper(goal_state)
        return path


class Node:
    def __init__(self, state, g, parent, direction, goal_state_hash):
        self.state = state
        self.g = g
        self.parent = parent
        self.direction = direction
        self.h = self.get_manhattan_dis(state, goal_state_hash)
        self.f = self.h + g
        self.goal_state_hash = goal_state_hash
        self.n = len(state)

    def __lt__(self, other):
        return self.g > other.g

    def __hash__(self):
        return hash(str(self.state))

    # Heuristic: Manhattan Distance
    def get_manhattan_dis(self, state, goal_state_hash):
        manhattan_dis = 0

        for i in range(0, len(state)):
            for j in range(0, len(state)):
                if state[i][j] != 0:
                    goal_coords = goal_state_hash[state[i][j]]
                    manhattan_dis += abs(goal_coords[0] - i) + \
                        abs(goal_coords[1] - j)

        return manhattan_dis

    def get_neighbors(self):
        row_of_zero = -1
        col_of_zero = -1
        neighbors = []

        for i in range(0, n):
            for j in range(0, n):
                if self.state[i][j] == 0:
                    row_of_zero = i
                    col_of_zero = j
                    break

        # Index of the cell + direction of movement
        up_index = [row_of_zero - 1, col_of_zero, "DOWN"]
        down_index = [row_of_zero + 1, col_of_zero, "UP"]
        left_index = [row_of_zero, col_of_zero - 1, "RIGHT"]
        right_index = [row_of_zero, col_of_zero + 1, "LEFT"]

        choices = [up_index, down_index, left_index, right_index]

        for choice in choices:
            if choice[0] < 0 or choice[1] < 0 or choice[0] >= n or choice[1] >= n:
                continue

            neighbor_state = [list(i) for i in self.state]
            neighbor_state[row_of_zero][col_of_zero] = self.state[choice[0]][choice[1]]
            neighbor_state[choice[0]][choice[1]] = 0

            neighbor_state_tuple = tuple(tuple(i) for i in neighbor_state)

            neighbors.append(Node(neighbor_state_tuple, self.g + 1, self,
                                  choice[2], self.goal_state_hash))

        return neighbors


class Bucket:
    def __init__(self):
        self.dict = {}
        self.min = 0
        self.n = 0

    def push(self, node):
        f_cost = node.f

        if self.dict.get(f_cost):
            heapq.heappush(self.dict[f_cost], node)
        else:
            self.dict[f_cost] = []
            heapq.heapify(self.dict[f_cost])
            heapq.heappush(self.dict[f_cost], node)

        self.n += 1

        if f_cost < self.min:
            self.min = f_cost

    def pop(self):

        if self.dict.get(self.min) and len(self.dict[self.min]) > 0:
            # print("Min: ", self.min)
            # print("Max: ", max(self.dict, key=int))
            # print("Key Size: ", len(self.dict.keys()))
            # print("Dict Size: ", len(self.dict[self.min]))
            ans = heapq.heappop(self.dict[self.min])
            # print("g: ", ans.g)
            self.n -= 1
            return ans
        else:
            # print("#######################################################")
            self.dict.pop(self.min, None)
            self.min = min(self.dict, key=int)
            if self.dict.get(self.min) and len(self.dict[self.min]) > 0:
                ans = heapq.heappop(self.dict[self.min])
                # print("g: ", ans.g)
                # print("Min: ", self.min)
                # print("Max: ", max(self.dict, key=int))
                # print("Key Size: ", len(self.dict.keys()))
                # print("Dict Size: ", len(self.dict[self.min]))
                self.n -= 1
                return ans

            return False


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

