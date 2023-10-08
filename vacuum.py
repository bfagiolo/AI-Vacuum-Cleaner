from tkinter import *
from collections import deque

#current location of the agent
cur_row = 0
cur_col = 0
#location of the dirt. -999 means room is clean.
dirt_row = -999
dirt_col = -999

# To track how many moves it takes
move_count = 0

# breadth-first search function
def bfs(graph, start, target):
    queue = deque([start])
    visited = set()

    while queue:
        x, y, path = queue.popleft()

        if (x, y) == target:
            return path

        if (x, y) in visited:
            continue

        visited.add((x, y))

        # Vacuum can only move up, down, left, right
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in moves:
            new_x, new_y = x + dx, y + dy
            queue.append((new_x, new_y, path + [(new_x, new_y)]))

    return None  # if Target square not found


def is_valid(x, y):
    return 0 <= x < 4 and 0 <= y < 4


# depth-first search function
def dfs(graph, start, target):
    stack = [start]
    visited = set()

    while stack:
        x, y, path = stack.pop()

        if (x, y) == target:
            return path

        if (x, y) in visited:
            continue

        visited.add((x, y))

        # Vacuum can move up, down, left, right
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in moves:
            new_x, new_y = x + dx, y + dy
            if is_valid(new_x, new_y):
                stack.append((new_x, new_y, path + [(new_x, new_y)]))

    return None  # if Target square not found


# Represents room layout with 4x4 squares
graph = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
]

# Move function for Vacuum
def move ():
    global dirt_row
    global dirt_col
    global cur_row
    global cur_col
    global static_move_row
    global static_move_col
    global move_count
    global path_breadth
    global path_depth
    
    move_count = 0      # Reset the move count
    
    start = (cur_row, cur_col, [(cur_row, cur_col)])    # Make start position the most recent position
    target = (dirt_row, dirt_col)
    path_breadth = bfs(graph, start, target)
    path_depth = dfs(graph, start, target)
    if len(path_breadth) < len(path_depth):     #compare bfs and dfs search
        path = path_breadth
    else:
        path = path_depth
    static_move_row = [item[0] for item in path]       # Make list for row moves
    static_move_col = [item[1] for item in path]       # Make list for column moves
    
    for item in path:
        # Removing the image from the button
        b[cur_row][cur_col].config(image='', height=4, width=8)
       
        # Adding the image to a new button and increasing the size 
        b[static_move_row[move_count]][static_move_col[move_count]]["image"] = icon
        b[static_move_row[move_count]][static_move_col[move_count]]["height"] = 100
        b[static_move_row[move_count]][static_move_col[move_count]]["width"] = 100
        root.update()
        root.after(350)
        # setting to a new current position for the agent
        cur_row = static_move_row[move_count]
        cur_col = static_move_col[move_count]
        
        move_count = move_count + 1
        
        # Checking to see if agent reaches to the Goal position
        if dirt_row == cur_row and dirt_col == cur_col:
            if len(path_breadth) < len(path_depth):
                label.config(text=f"Clean. Total move: {move_count-1} . Used BFS")
            else:
                label.config(text=f"Clean. Total move: {move_count-1} . Used DFS")
            clean_button.config(state="disabled")
            b[dirt_row][dirt_col]["text"] = "" 
        
    
    
# This function makes a location dirty
def clicked(row, col):
    # Agent current location cannot be dirty
    if cur_row == row and cur_col == col:
        return;
    
    b[row][col]["text"] = "Dirt"    # labeling dirt location
    
    global dirt_row
    global dirt_col
    
    # Marking dirt location
    dirt_row = row
    dirt_col = col
    
    clean_button.config(state="active")   # Clean button is enabled
    

root = Tk()
root.title("Room")
root.geometry("800x500")
# 16 buttons for the 16 locations
b = [
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
]

icon = PhotoImage(file='/Users/brandonfagiolo/Desktop/AI Programming/vacuum_pic.png')

for i in range(4):
    for j in range(4):
        b[i][j] = Button(       
                        height = 4, width = 8,
                        font = ("Helvetica", "20"),
                        command = lambda r = i, c = j : clicked(r,c))
        b[i][j].grid(row=i,column=j)

# Make the first button bigger and adding picture of the agent 
b[0][0]["image"] = icon
b[0][0]["height"] = 100
b[0][0]["width"] = 100

# Add another button on the right side
clean_button = Button(
    text="Clean",
    state="disabled",
    height=4, width=8,
    font=("Helvetica", "20"),
    command = move
)

clean_button.grid(row=0, column=4)

# Add a label on the right side
label = Label(
    text="",
    font=("Helvetica", "17")
)
label.grid(row=1, column=4)

mainloop()
