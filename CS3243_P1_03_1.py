import os
import sys
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

        #finding index of 0
        for r in range(row_len):
            for c in range(row_len):
                if(init_state[r][c] == 0):
                    index = (r,c)
                    break
        #one time check for solvability
        if(self.unsolvable_check(init_state,row_len,index)):
            self.actions.append("UNSOLVABLE")
            return self.actions

        visited_nodes = {0}
        frontier = list()
        #frontier will hold the state of a node, the index of 0 and the list of actions to get there
        frontier.append((init_state,index,self.actions))

        while len(frontier):
            state = frontier.pop(0)
            converted_arr = self.convert(state[0],row_len)

            if converted_arr in visited_nodes:
                continue

            actions_len = len(state[2])
            if(actions_len):
                last_action = state[2][actions_len-1]
            else:
                last_action = "NO ACTIONS"

            #shifting upper block down to blank
            if(state[1][0] != 0 and last_action != "UP"):
                temp_state, temp_actions = self.tempCopy(state[0],state[2])
                result_state = self.down(temp_state,state[1])
                result_index = (state[1][0]-1,state[1][1])
                temp_actions.append("DOWN")
                if(self.goal_check(result_state,result_index,temp_actions,frontier)):
                    break
            #shifting lower block up to blank
            if(state[1][0] != row_len-1 and last_action != "DOWN"):
                temp_state, temp_actions = self.tempCopy(state[0],state[2])
                result_state = self.up(temp_state,state[1])
                result_index = (state[1][0]+1,state[1][1])
                temp_actions.append("UP")
                if(self.goal_check(result_state,result_index,temp_actions,frontier)):
                    break
            #shifting block left on to blank
            if(state[1][1] != row_len-1 and last_action != "RIGHT"):
                temp_state, temp_actions = self.tempCopy(state[0],state[2])
                result_state = self.left(temp_state,state[1])
                result_index = (state[1][0],state[1][1]+1)
                temp_actions.append("LEFT")
                if(self.goal_check(result_state,result_index,temp_actions,frontier)):
                    break           
            #shifting block right on to blank
            if(state[1][1] != 0 and last_action != "LEFT"):
                temp_state, temp_actions = self.tempCopy(state[0],state[2])
                result_state = self.right(temp_state,state[1])
                result_index = (state[1][0],state[1][1]-1)
                temp_actions.append("RIGHT")
                if(self.goal_check(result_state,result_index,temp_actions,frontier)):
                    break

            visited_nodes.add(converted_arr)

        tock = time.time()
        print(tock-tick)
        return self.actions

    def goal_check(self,result_state,result_index,temp_actions,frontier):
        if((result_state) == goal_state):
            self.actions = temp_actions
            return True
        frontier.append((result_state,result_index,temp_actions))

    def tempCopy(self,state,actions):
        temp_state = [i[:] for i in state]
        temp_actions = actions[:]
        return temp_state, temp_actions

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
        arr_string = ""
        for r in range(row_len):
            for c in range(row_len):
                arr_string = arr_string + str(state[r][c])
        return arr_string

    #Since n == 3, if inversion_check returns an odd number, the puzzle is unsolvable
    def unsolvable_check(self,state,row_len,index):
        inversion_count = 0
        for num in range(1,(row_len*row_len)-1):
            row = 0
            col = 0
            while(state[row][col] != num):
                if(state[row][col] == 0 or state[row][col] < num):
                    pass
                else:
                    inversion_count += 1
                if(col != row_len-1):
                    col += 1
                elif(row != row_len-1):
                    row += 1
                    col = 0
                else:
                    break
        # if row_len odd and odd inversions                    
        if(row_len%2):
            if(inversion_count%2):
                return True
        else:
            # if row_len even, 0 on even row from bottom and even inversions
            if((row_len-1-index[0])%2 and inversion_count%2 == 0):
                return True
            # if row_len even, 0 on odd row from bottom and odd inversions
            elif((row_len-1-index[0]%2 == 0 and inversion_count%2)):
                return True


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







