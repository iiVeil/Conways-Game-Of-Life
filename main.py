import os
import time

# time between iterations
timeBetween = 500

# board size || [length, height]
size = [25, 10]

# tile states || [dead, alive]
states = ["□", "■"]

# declare board || board[y][x]
board = [[False for x in range(size[0])] for y in range(size[1])]
saved_board = []

# create the shown board
def make():
    active = ""
    for line in board[::-1]:
        x = 0
        for cell in line:
            if x != size[0] - 1:
                active += f"{states[0]} " if cell == False else f"{states[1]} "
            else:
                active += f"{states[0]}\n" if cell == False else f"{states[1]}\n"
            x += 1
    print(active)

# change board size
def edit(pair):
    global board, size
    y,x = pair[0], pair[1]
    size = [y, x]
    board = [[False for x in range(size[0])] for y in range(size[1])]

# gets the state of any given coordinates
def get_state(pair):
    y,x = pair[0]-1, pair[1]-1
    return "Dead" if board[y][x] == False else "Alive"

# checks if any pair of coordinates is on the board
def on_board(pair):
    y,x = pair[0]-1, pair[1]-1
    return True if size[1]-1 >= y and size[0]-1 >= x and y >= 0 and 0 <= x else False

# clears the terminal
def clear(): 
    # windows 
    if os.name == 'nt': 
        os.system('cls') 
    # mac & linux
    else: 
        os.system('clear') 

# swaps the state of any given coordinates
def swap_state(pair):
    y,x = pair[0]-1, pair[1]-1
    board[y][x] = not board[y][x]
    return "Alive" if board[y][x] == True else "Dead"

# find the neighbors of a pair, returns a dict of the amount of alive and dead neighbors
def neighbors(pair):
    y,x = pair[0], pair[1]
    neigh = {"Alive": 0}
    # top right, bottom left, bottom right, top left, left, right, top, bottom
    checks = [[y+1, x+1],[y-1, x-1],[y-1, x+1],[y+1, x-1],[y, x-1],[y, x+1],[y+1, x],[y-1, x]]
    for pos in checks:
        if on_board(pos):
            if get_state(pos) == "Dead":
                continue
            neigh[get_state(pos)] += 1
    return neigh

# iterate cells
def iterate():
    swaps, alive, dead = [], [], []

    # get all dead and alive cells on the board and seperate them
    y = 0
    for line in board:
        y += 1
        x = 0
        for cell in line:
            if cell == False:
                dead.append([y,x+1])
            else:
                alive.append([y,x+1])
            x += 1
    # Checks rules for all alive cells
    for cell in alive:
        lon = neighbors(cell)
        if lon["Alive"] < 2:
            swaps.append(cell)
            continue
        elif lon["Alive"] == 2 or lon["Alive"] == 3:
            continue
        elif lon["Alive"] > 3:
            swaps.append(cell)
            continue
    
    # Checks rules for all dead cells
    for cell in dead:
        lon = neighbors(cell)
        if lon["Alive"] == 3:
            swaps.append(cell)
            continue

    for cell in swaps:
        swap_state(cell)
        

    

# parses commands given
def parse(inp):
    global timeBetween
    # clears command window
    clear()
    
    # quit command
    if inp.lower() == "quit":
        quit()
    elif inp.lower() == "reload":
        if saved_board == []:
            return print("No board saved. Try iterating!")
    # change time before iterations
    elif inp.isdigit():
        if int(inp) > 0 and int(inp) <= 5000:
            timeBetween = int(inp)
        elif int(inp) > 5000:
            return print("Iteration time to high!")
    
    # change board size
    elif "x" in inp.lower() and inp.lower().split("x")[0].isdigit() and inp.lower().split("x")[1].isdigit():
        coords = int(inp.lower().split("x")[1]), int(inp.lower().split("x")[0])
        edit(coords)
    
    # iterate command
    elif inp.lower().startswith("iterate ") and inp.lower().split(" ")[1].isdigit():
        am = int(inp.lower().split(" ")[1])
        while am > 0:
            iterate()
            print(f"Size: {size[1]}x{size[0]}")
            print(f"Time between iterations: {timeBetween}ms ({timeBetween/1000}s)")
            print("Compass:\n    +h   \n -l    +l \n    -h   \n\n")
            make()
            time.sleep(timeBetween/1000)
            am -= 1
            clear()
    # help command
    elif inp.lower() == "help":
        return print("help - Shows this menu\nclear - Clears the board\nquit - Quits program\n[height],[length] - Changes cell state based on coordinates\n[1-5000] - Sets the time between iterations in MS (1000ms = 1 second)\niterate [num] - Number of times to iterate board (starts iteration)\n[height]x[length] - Changes the size of the board, will wipe board\nreload - reloads the state of the board before iteration\n\n=================================================\n")
    elif inp.lower() == "clear":
        edit(size)
    # parses coordinates [Y,X]
    elif "," in inp and inp.split(",")[0].isdigit() and inp.split(",")[0].isdigit():
        coords = [int(inp.split(",")[0]), int(inp.split(",")[1])]
        if coords[0]-1 < 0 or coords[1]-1 < 0:
            return print("Invalid coords, origin is (1,1) bottom left")
        return swap_state(coords) if on_board(coords) else print("Not on board!")
    else:
        return print("Invalid command.") 
print(f"Size: {size[1]}x{size[0]}")
print(f"Time between iterations: {timeBetween}ms ({timeBetween/1000}s)")
print("Compass:\n    +h   \n -l    +l \n    -h   \n\n")
make()

while True:
    parse(input("Command: "))
    print(f"Size: {size[1]}x{size[0]}")
    print(f"Time between iterations: {timeBetween}ms ({timeBetween/1000}s)")
    print("Compass:\n    +h   \n -l    +l \n    -h   \n\n")
    make()
