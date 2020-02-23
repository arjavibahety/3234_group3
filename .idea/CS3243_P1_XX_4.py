import os
import sys
import time
import heapq


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()
        self.n = len(init_state)

    def solve(self):
        # implement your search algorithm here
        start_time = time.time()
        if not self.is_solvable(init_state):
            print("--- %s seconds ---" % (time.time() - start_time))
            return ["UNSOLVABLE"]

        goal_state_hash = self.get_goal_state_hash(goal_state)
        goal_state_tuple = tuple(tuple(i) for i in goal_state)

        start_node = Node(tuple(tuple(i) for i in init_state), 0, False, False, goal_state_hash)
        frontier = []
        visited = {}
        heapq.heapify(frontier)
        heapq.heappush(frontier, start_node)
        goal_node = False
        current = True

        while len(frontier) > 0:
            current = heapq.heappop(frontier)

            if visited.get(current.state) and visited[current.state].g < current.g:
                continue
            visited[current.state] = current

            # Goal State reached
            if self.is_equal_states(current.state, goal_state_tuple):
                goal_node = current
                break

            neighbors = current.get_neighbors()

            for neighbor in neighbors:
                if visited.get(neighbor.state):
                    continue
                heapq.heappush(frontier, neighbor)
        path = self.get_path(goal_node.state, visited)

        print("Goal Node State: ", goal_node.state)
        print('Time taken: {duration}'.format(duration=(time.time() - start_time)))

        return path


    #This function returns true if puzzle is solvable, false otherwise.
    def is_solvable(self, init_state):
        inversions = 0
        arr = []
        row_with_zero = -1
        n = len(init_state)


        for i in range(0, self.n):
            for j in range (0, self.n):
                arr.append(init_state[i][j])
                if init_state[i][j] == 0:
                    row_with_zero = i

        for i in range(0, len(arr)):
            for j in range (0, i):
                if arr[i] < arr[j] and arr[i] != 0 and arr[j] != 0:
                    inversions += 1

        # If puzzle length is odd and inversions is even, return True for solvable
        if n % 2 == 1:
            return inversions % 2 == 0
        else:
            # If puzzle length is even and inversions + row with zero is odd, return True for solvable
            return (inversions + row_with_zero) % 2 == 1

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

        def helper(state):
            current = visited[state]
            if current.parent:
                helper(current.parent.state)
                path.append(current.direction)
        helper(goal_state)
        return path
class Node(object):
    def __init__(self, state, g, parent, direction, goal_state_hash):
        self.state = state
        self.g = g
        self.parent = parent
        self.direction = direction
        self.n = len(state)
        self.goal_state_hash = goal_state_hash

    def __lt__(self, other):
        return self.g < other.g

    def __hash__(self):
        return hash(str(self.state))


    def has_state_equals_to(self, other_state):
        is_equals = True
        for i in range (0, self.n):
            for j in range (0, self.n):
                if self.state[i][j] != other_state[i][j]:
                    is_equals = False
                    break

        return is_equals

    def get_heuristic_cost(self):
        return self.__get_max_sort()

        # Heuristic: N-MaxSwap. Num of tiles needed to be swapped to reach the goal state
    # if it were possible to swap any tile with the '0' tile.
    def get_max_swap(self):
        swap = 0
        i = 0
        array_size = self.n * self.n
        array = [0 for i in range(array_size)]
        for j in range (0,self.n):
            for k in range(0, self.n):
                array[i] = self.state[j][k]
                i += 1

        #swap '0' with any tile
        for j in range (0,len(array)):
            value = array[j]
            if value == 0:
                # '0' is at the correct place but unsorted
                smallest_unsorted_num = len(array)
                if(j == len(array) - 1): #If '0' is at the correct place
                    for k in range(0, array_size-2):
                        if array[k] != k+1: #unsorted
                            if(array[k] < smallest_unsorted_num):
                                smallest_unsorted_num = array[k]

                value_to_swap_with = j+1
                for k in range(0, len(array)):
                    if array[k] == value_to_swap_with:
                        array[j] = value_to_swap_with
                        array[k] = 0
                        swap += 1
                        break
        return swap

    def get_neighbors(self):
        zero_row = -1
        zero_col = -1
        neighbors= []

        for i in range (0, self.n):
            for j in range (0, self.n):
                if self.state[i][j] == 0:
                    zero_row = i
                    zero_col = j
                    break

        left_index = [zero_row, zero_col - 1, "RIGHT"]
        right_index = [zero_row, zero_col + 1, "LEFT"]
        up_index = [zero_row - 1, zero_col, "DOWN"]
        down_index = [zero_row + 1, zero_col, "UP"]

        indices = [left_index, right_index, up_index, down_index]

        for index in indices:
            if index[0] < 0 or index[1] < 0 or index[0] >= n or index[1] >= n:
                continue
            neighbor_state = [list(i) for i in self.state]
            neighbor_state[zero_row][zero_col] = neighbor_state[index[0]][index[1]]
            neighbor_state[index[0]][index[1]] = 0

            neighbor_state_tuple = tuple(tuple(i) for i in neighbor_state)

            neighbors.append(Node(neighbor_state_tuple, self.g + 1, self, index[2], self.goal_state_hash))

        return neighbors




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
