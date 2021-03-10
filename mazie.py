import copy
import getpass
import sys
import telnetlib

HOST = "54.170.244.112"
PORT = "1337"

testMaze = "+---+---+---+---+---+---+---+\n| S                     |   |\n+   +---+---+---+---+   +   +\n|   |                   |   |\n+   +   +---+---+---+---+   +\n|   |   |       |           |\n+   +   +   +   +---+---+   +\n|   |       |           |   |\n+---+---+---+---+---+   +   +\n|       |           |       |\n+   +   +   +---+   +---+   +\n|   |   |   |   |           |\n+   +---+   +   +---+---+---+\n|                         F |\n+---+---+---+---+---+---+---+"


def print_maze(maze):
    for m in maze:
        print(m)


def process_maze(maze):
    matrix_maze = []
    for line in maze.split('\n'):
        matrix_maze.append(line)
    return matrix_maze


def solve(maze):
    return pathTrace(maze, 2, 2, None)


def pathTrace(maze, x, y, d):
    posX = x
    posY = y
    actions = []
    actions.append(d) if d is not None else None
    maze = update_maze(maze, posX, posY, d) if d is not None else maze
    while True:
        if maze[posX][posY] == 'F':
            return True, copy.deepcopy(maze)

        directions = available_directions(maze, posX, posY)
        if len(directions) == 0:
            return False, ""
        if len(directions) == 1:
            actions.append(directions[0])
            actions.append(directions[0]) if maze[posX][posY] != 'S' else None
            posX, posY = direction_move(posX, posY, directions[0])
            maze = update_maze(maze, posX, posY, directions[0])
            d = directions[0]
        else:
            for dir in directions:
                temp_x, temp_y = direction_move(posX, posY, dir)
                found, newmaze = pathTrace(copy.deepcopy(maze), temp_x, temp_y, dir)
                if found:
                    return True, newmaze
            return False, ""


def update_maze(maze, x, y, action):
    if action == None:
        return maze

    if action == ">":
        #maze = place_action(maze, x, y, action)
        maze = place_action(maze, x, y - 2, action)
        maze = place_action(maze, x, y - 4, action)

    if action == "<":
        #maze = place_action(maze, x, y, action)
        maze = place_action(maze, x, y + 2, action)
        maze = place_action(maze, x, y + 4, action)

    if action == "^":
        #maze = place_action(maze, x, y, action)
        maze = place_action(maze, x + 1, y, action)
        maze = place_action(maze, x + 2, y, action)

    if action == "V":
        #maze = place_action(maze, x, y, action)
        maze = place_action(maze, x - 1, y, action)
        maze = place_action(maze, x - 2, y, action)

    return maze


def place_action(maze, x, y, action):
    temp = list(maze[x])
    action = action.lower()
    if temp[y] == " ":
        temp[y] = action
    maze[x] = "".join(temp)
    return maze


def flip_direction(d):
    if d == '>':
        return '<'
    if d == '<':
        return '>'
    if d == 'V':
        return '^'
    if d == '^':
        return 'V'


def direction_move(x, y, d):
    if d == '>':
        return (x , y + 4)
    if d == '<':
        return (x, y - 4)
    if d == 'V':
        return (x + 2, y)
    if d == '^':
        return (x - 2, y)


def available_directions(maze, x, y):
    directions = []
    if maze[x][y - 2] == ' ':
        directions.append('<')

    if maze[x][y + 2] == ' ':
        directions.append('>')

    if maze[x - 1][y] == ' ':
        directions.append('^')

    if maze[x + 1][y] == ' ':
        directions.append('V')

    return directions


def render_maze(maze):
    temp = ""
    for m in maze:
        temp += m + "\n"
    return temp

#print(testMaze)
#print_maze(pathTrace(process_maze(testMaze), 1, 2, None)[1])
#exit()
tn = telnetlib.Telnet(HOST, PORT)
tn.write(b"\n")
tn.read_until(b'[Enter  to continue ...]')
tn.write(b"\n")

print(tn.read_until(b'Choice:'))
tn.write(b"2\n")
tn.read_until(b'First we need to escape the first maze:\n')
maze = tn.read_until(b'+---+---+---+---+---+---+---+')
maze += tn.read_until(b'+---+---+---+---+---+---+---+')
maze = maze.decode("utf-8")
print("begin")
for line in maze.split('\n'):
    print(line)
print("end")
result = pathTrace(process_maze(maze), 1, 2, None)
print(result)
send = render_maze(pathTrace(process_maze(maze), 1, 2, None)[1])
tn.write(str.encode(send + "\n"))
print(str.encode(send))
print(send)


tn.read_until(b'[Enter  to continue ...]')
tn.write(b"\n")

tn.read_until(b'I think so...\n')
maze = tn.read_until(b'+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+')
maze += tn.read_until(b'+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+')
maze = maze.decode("utf-8")

send = render_maze(pathTrace(process_maze(maze), 1, 2, None)[1])
tn.write(str.encode(send + "\n"))
print(str.encode(send))
print(send)


tn.read_until(b'[Enter  to continue ...]')
tn.write(b"\n")

tn.read_until(b'I can see the outside light!\n')
maze = tn.read_until(b'+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+')
maze += tn.read_until(b'+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+')
maze = maze.decode("utf-8")


send = render_maze(pathTrace(process_maze(maze), 1, 2, None)[1])
tn.write(str.encode(send + "\n"))
print(str.encode(send))
print(send)

tn.interact()

