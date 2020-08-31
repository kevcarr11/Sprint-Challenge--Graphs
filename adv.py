from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


def opposite_direction(direction):
    # back track to unvisited exits
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'e':
        return 'w'
    elif direction == 'w':
        return 'e'


# create a empty stack to use for DFT
paths = Stack()
# rooms that we have visited
visited = set()

traversal_path = []

# compare number of visited rooms to number of rooms to ensure complete traversal
while len(visited) < len(world.rooms):
    # get all possible exits for current room
    exits = player.current_room.get_exits()
    # print('Room:', player.current_room)
    # print('exits are', exits)

    # create empty list to keep track of the exits we take
    current_path = []

    # loop through each possible exit and check if visited before
    for exit in exits:
        # if exit exists and we haven't visited room yet
        if exit is not None and player.current_room.get_room_in_direction(exit) not in visited:
            # add that exit to the current_path
            current_path.append(exit)
            # print('current_path', current_path)

    # add current room to visited
    visited.add(player.current_room)

    if len(current_path) > 0:
        # pick a random unexplored direction from the player's current room and push onto stack
        random_index = random.randint(0, len(current_path) - 1)
        paths.push(current_path[random_index])
        # advance player current room in the chosen direction
        player.travel(current_path[random_index])
        # add chosen direction to traversal path
        traversal_path.append(current_path[random_index])
        # print('more rooms to explore')
    else:
        # reached the end of current path, time to back track
        # pop from stack to get the last direction taken
        end = paths.pop()
        # back track player in that direction and add to traversal path as traveled
        player.travel(opposite_direction(end))
        traversal_path.append(opposite_direction(end))
        # print('this is the end of current path')


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
