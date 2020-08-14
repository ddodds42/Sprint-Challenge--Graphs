from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# import sys
# sys.path.insert(1, '../graph/')
# from graph import Graph

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
# world.load_graph(room_graph)

'''rooms is for modificaiton by links, forks, and bridges'''
rooms = set(room_graph.keys())
'''links are rooms with only 2 neighboring rooms'''
links = rooms.copy()

'''leaves are leaf nodes, or dead end rooms with only 1 neighbor'''
leaves = set()
'''forks have 3 or more neightbors. these rooms are divergence points that must
be returned to in a traversal or search'''
forks = set()

'''this loop sorts rooms into leaves, links, and forks'''
for i in list(room_graph.keys()):
    if len(room_graph[i][1]) < 2:
        leaves.add(i)
        links.remove(i)
    elif len(room_graph[i][1]) > 2:
        forks.add(i)
        links.remove(i)

'''this directory is the beginning of a dictionary that will allow each room to
become a graph object that may be traversed with methods built earlier in the
week.'''
directory = room_graph.copy()

'''this helper function swaps the key-value pairs in the each room's dicitonary
so now each key is the name of the neighboring room, and its value is the
direction you head to get to that neighbor.'''
def swapper(dict_value):
    holder = {}
    for k in dict_value[1].keys():
        holder[dict_value[1][k]] = k
    dict_value[1] = holder
    return dict_value

'''this loop populates each rooms dict in directory with the swapped values.'''
for i in directory:
    directory[i] = swapper(directory[i])

print(directory)