#Douglas Adjei-Frempah - dadje001 - 862259280
#Program to solve 8 puzzle 
#uniform cost search
#A* with misplaced tile heuristic 
#A* with the mdh Distance heuristic heuristic
#remember to use these variables ={make_queue, make_node, initial_state, empty, remove_front
# , goal_test, state, queueing_function, operators} where possible
#use flatlist instead of a grid numpy array 

#High level help was solicited from Harsh Patel, some modules/functions were influenced and refined by readings and articles 
#from www.programiz.com , geeksforgeeks.com, stackoverflow answers and a few others

import copy 
import time
import sys


#initializing a grid system to utilize for computing boundaries and allowed movements across rows and columns
board_size =3 #3x3 Grid system
default_puzzle = (['1', '2', '3'], ['4', '0', '6'], ['7', '5', '8'])
goal_puzzle = (['1', '2', '3'], ['4', '5', '6'], ['7', '8', '0'])
sanity = True 

def main():
    #getting the user input as a single complete string and processing it
    print(""" Enter board current state as a list of 9 consecutive elements, 
    Kindly do not leave SPACES and use 0 to indicate the blank space 
    E.g 1 
    [6, 4, 1
     2, 3, 5
     0, 7, 8 ] should be entered as "641235078" followed by the enter key

    If you want to use the default board, enter "0"
    """)
    input_sequence = input("Enter as a combined string here or \"0\" for default: ")
    


    # Creating a default puzzle in case users do not want to input their own puzzle instance
    if input_sequence == "0":
        puzzle = default_puzzle
    elif len(input_sequence) == 9:
        puzzle = list(input_sequence[0:3]), list(input_sequence[3:6]), list(input_sequence[6:9]) #treating the single string user input into a three member tuple for easy use 
    else: 
        print("Wrong input. Restart the program")
        sys.exit(0)

    print(puzzle)

#getting the choice of heuristic from the user
    print("""
        Choose the Heuristic you want to use 
        1 = Uniform cost search 
        2 = Misplaced tiles as heuristic for A-star 
        3 = Manhattan distance as heurisitic for A-star
    """)
    choice = input("Heuristic option(Enter 1 number): ")

   
    h_choice = int(choice)

  #executing the search function
    print(generalsearch(puzzle, h_choice))


#this function tests for which movements or operators are permitted in any given state
def movement(current_node, prev_seen):
    valid_moves = { 
        "isLeftPossible": True, 
        "isRightPossible": True, 
        "isUpPossible": True, 
        "isDownPossible": True
    }
    
    blank_x = blank_y = 0   #row and column values for the blank spot which moves across the game board

    for i in range(len(current_node.puzzle)): 
        for j in range(len(current_node.puzzle)): 
            if int(current_node.puzzle[i][j]) == 0: 
                blank_x, blank_y = i, j #ascertaining exactly were our blank tile resides
    
    if blank_x > 0: # we can move up if this holds
        valid_moves["isUpPossible"] = True
    if blank_x < (board_size - 1): #we can move down if this holds
        valid_moves["isDownPossible"] = True
    if blank_y < (board_size - 1) : #we can move right
        valid_moves["isRightPossible"] = True 
    if blank_y > 0: #we can move left
        valid_moves["isLeftPossible"] = True
    

#performing deep copies using pythons deep copy module since we want more than shallow references
#and thereafter performing move operations which are permitted based on the postion of the tile
    if blank_y > 0:
        push_left = copy.deepcopy(current_node.puzzle)
        push_left[blank_x][blank_y], push_left[blank_x][blank_y - 1] = push_left[blank_x][blank_y - 1] , push_left[blank_x][blank_y] 
        current_node.child1 = node(push_left)

   
    if blank_y < board_size - 1:

        push_right = copy.deepcopy(current_node.puzzle)
        push_right[blank_x][blank_y], push_right[blank_x][blank_y + 1] = push_right[blank_x][blank_y + 1] , push_right[blank_x][blank_y]
        if push_right not in prev_seen:
            current_node.child2 = node(push_right)


    if blank_x > 0:
        push_up = copy.deepcopy(current_node.puzzle)
        push_up[blank_x][blank_y], push_up[blank_x - 1 ][blank_y] = push_up[blank_x - 1][blank_y], push_up[blank_x][blank_y]
        if push_up not in prev_seen:
            current_node.child3 = node(push_up)

    if blank_x < board_size -  1:
        push_down = copy.deepcopy(current_node.puzzle)
        push_down[blank_x][blank_y] , push_down[blank_x + 1][blank_y] = push_down[blank_x + 1][blank_y], push_down[blank_x][blank_y]
        current_node.child4 = node(push_down)

    return current_node

class node:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.heuristic_cost = 0
        self.depth = 0
        self.child1 = None
        self.child2 = None
        self.child3 = None
        self.child4 = None
        self.expanded = False

        #4 children becuase there is a max of 4 branches to each node
        
#generic search algorithm
def generalsearch(problem, h_choice):
    init_time = time.time() #tracking how long the search action takes
    
    queue = []
    seen = []
    nodeCount = -1
    queuesize = 0
    max_queue_size = -1

    # Calculating heuristic based on the user inputted heuristic
    if h_choice == 1:
        h = 0 #with h hardcoded to 0 this heuristic devolves to uniform cost search
    if h_choice == 2:
        h = mth(problem) 
    if h_choice == 3:
        h = mdh(problem)

    # Creating the start node, with the puzzle, depth of 0, and heuristic. We then add the node to the queue
    # and list it in the seen array.
    n = node(problem)
    n.heuristic_cost = h
    n.depth = 0
    queue.append(n)

    seen.append(n.puzzle)
    queuesize +=1
    max_queue_size += 1

    
 
    while sanity: #initialize a true value so we can loop till we are done
        # Sort the queue for the lowest h(n) + g(n)
        if h_choice != 1:
            queue = sorted(queue, key=lambda x: (x.depth + x.heuristic_cost, x.depth))
        # If the queue is empty we can't do anything
        if len(queue) == 0:
            return 'Failure :('
#pop the first node and further increment the number of visited/explored nodes
        current_node = queue.pop(0)
        if current_node.expanded is False:
            nodeCount += 1
            current_node.expanded = True
        queuesize -= 1

        # Display important search metrics upon success
        if success(current_node.puzzle):
            elapsed = time.time() - init_time
            return(f"""
                Search complete!!!
                Final Node:  \n
                Total nodes explored: {nodeCount}
                Largest Queue Size: {max_queue_size}
                Depth of Solution: {current_node.depth} 
                Time elapsed: {elapsed} seconds
            """)

        if nodeCount != 0:
            print('Least G(n)' + str(current_node.depth))
            print('Least H(n)' + str(current_node.heuristic_cost))
            print("Best Node: \n")
            illustrateBoard(current_node.puzzle)
        else:
            print("Best Node: \n")
            illustrateBoard(current_node.puzzle)
           

        full_explore = movement(current_node, seen) 

        # Loop through the array of children and modify stats based on the expanded puzzles based on heuristics chosen
        # by the user. The depth is the depth of the parent node (node popped off queue + 1).
        arr = [full_explore.child1, full_explore.child2, full_explore.child3, full_explore.child4]

        for i in arr:
            if i is not None:
                if h_choice == 1:
                    i.depth = current_node.depth + 1
                    i.heuristic_cost = 0
                elif h_choice == 2:
                    i.depth = current_node.depth + 1
                    i.heuristic_cost = mth(i.puzzle)
                elif h_choice == 3:
                    i.depth = current_node.depth + 1
                    i.heuristic_cost = mdh(i.puzzle)

                # Add these states to the queue and add them to a list of states we have now seen
                queue.append(i)
                seen.append(i.puzzle)
                queuesize += 1

        # Change the max queue size if it has been surpassed
        if queuesize > max_queue_size:
            max_queue_size = queuesize
        hardstop = 601

        if time.time() > init_time + hardstop:
            print('More than 10 minutes elapsed') #we dont let it run for more than 10 minutes
            sys.exit()

#mdh stands for manhattan distance heuristic
def mdh(puzzle):
    puzzle = puzzle[0] + puzzle[1] + puzzle[2]
    puzzle = [int(x) for x in puzzle]
    value = sum(abs((val-1)%3 - int(i)%3) + abs((val-1)//3 - int(i)//3)
        for i, val in enumerate(puzzle) if val)
    return value


#mth stands for misplaced tiles heuristic
def mth(puzzle): 
    value = 0 
    for i in range(board_size): #3 for 3x3 , 5 for 5x5 
        for j in range(board_size): 
            if puzzle[i][j] != goal_puzzle[i][j]: 
                value += 1

    return value

def success(puzzle): 
    if puzzle == goal_puzzle: 
        return True
    else: 
        return False

def illustrateBoard(puzzle): 
    gridline_1 = f"| {puzzle[0][0]} {puzzle[0][1]} {puzzle[0][2]} |\n"
    gridline_2 = f"| {puzzle[1][0]} {puzzle[1][1]} {puzzle[1][2]} |\n"
    gridline_3 = f"| {puzzle[2][0]} {puzzle[2][1]} {puzzle[2][2]}|\n"
    print("\n" , gridline_1, gridline_2, gridline_3)


if __name__ == "__main__":
    main()
