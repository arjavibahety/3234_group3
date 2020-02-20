import os
import sys
import copy
import time

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()

    def solve(self):
        #consider flattening array into str for faster processing
        tick = time.time()
        row_len = len(init_state)

        #one time check for solvability
        if( (self.inversion_check(init_state,row_len)) % 2):
            print("UNSOLVABLE")
            return self.actions
        #finding index of 0
        for r in range(row_len):
            for c in range(row_len):
                if(init_state[r][c] == 0):
                    index = (r,c)
                    break

        visited_nodes = {0}
        frontier = list()
        #frontier will hold the state of a node, the index of 0 and the list of actions to get there
        frontier.append((init_state,index,self.actions))

        while len(frontier):
                state = frontier.pop(0)
                #print(state[0])
                converted_arr = self.convert(state[0],row_len)

                if converted_arr in visited_nodes:
                    continue

                #shifting upper block down to blank
                if(state[1][0] != 0):
                    temp_state = copy.deepcopy(state[0])
                    temp_actions = copy.copy(state[2])
                    result_state = self.down(temp_state,state[1])
                    result_index = (state[1][0]-1,state[1][1])
                    temp_actions.append("DOWN")
                    if((result_state) == goal_state):
                        self.actions = temp_actions
                        break
                    frontier.append((result_state,result_index,temp_actions))
                #shifting lower block up to blank
                if(state[1][0] != row_len-1):
                    temp_state = copy.deepcopy(state[0])
                    temp_actions = copy.copy(state[2])
                    result_state = self.up(temp_state,state[1])
                    result_index = (state[1][0]+1,state[1][1])
                    temp_actions.append("UP")
                    if((result_state) == goal_state):
                        self.actions = temp_actions
                        break
                    frontier.append((result_state,result_index,temp_actions))
                #shifting block right on to blank
                if(state[1][1] != 0):
                    temp_state = copy.deepcopy(state[0])
                    temp_actions = copy.copy(state[2])
                    result_state = self.right(temp_state,state[1])
                    result_index = (state[1][0],state[1][1]-1)
                    temp_actions.append("RIGHT")
                    if((result_state) == goal_state):
                        self.actions = temp_actions
                        break
                    frontier.append((result_state,result_index,temp_actions))
                #shifting block left on to blank
                if(state[1][1] != row_len-1):
                    temp_state = copy.deepcopy(state[0])
                    temp_actions = copy.copy(state[2])
                    result_state = self.left(temp_state,state[1])
                    result_index = (state[1][0],state[1][1]+1)
                    temp_actions.append("LEFT")
                    if((result_state) == goal_state):
                        self.actions = temp_actions
                        break
                    frontier.append((result_state,result_index,temp_actions))

                visited_nodes.add(converted_arr)

                #If exhaust all permutations
                if(len(visited_nodes) == 3628800):
                    print("UNSOLVABLE")
                
                #print(len(visited_nodes))
        print(self.actions)
        tock = time.time()
        print(tock-tick)
        return self.actions

    def down(self,state,index):
        state[index[0]][index[1]], state[index[0]-1][index[1]] = state[index[0]-1][index[1]], state[index[0]][index[1]]
        return state
    def up(self,state,index):
        state[index[0]][index[1]], state[index[0]+1][index[1]] = state[index[0]+1][index[1]], state[index[0]][index[1]]
        return state
    def left(self,state,index):
        state[index[0]][index[1]], state[index[0]][index[1]+1] = state[index[0]][index[1]+1], state[index[0]][index[1]]
        return state
    def right(self,state,index):
        state[index[0]][index[1]], state[index[0]][index[1]-1] = state[index[0]][index[1]-1], state[index[0]][index[1]]
        return state

    #convert state to string to put in set. For checking visited nodes
    def convert(self,state,row_len):
        arrString = ""
        for r in range(row_len):
            for c in range(row_len):
                arrString = arrString + str(state[r][c])
        return arrString

    #if inversion_check returns an odd number, the puzzle is unsolvable
    def inversion_check(self,state,row_len):
        row = 0
        col = 0
        inversion_count = 0
        for num in range(1,(row_len*row_len)-1):
            #print("Looking for " + str(num))
            row = 0
            col = 0
            while(state[row][col] != num):
                if(state[row][col] == 0):
                    pass
                elif(state[row][col] < num):
                    pass
                else:
                    #print("Caught " + str(state[row][col]))
                    inversion_count += 1
                if(col != row_len-1):
                    col += 1
                elif(row != row_len-1):
                    row += 1
                    col = 0
                else:
                    break
        return inversion_count

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







