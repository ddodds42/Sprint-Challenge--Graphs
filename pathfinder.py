from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

import sys
sys.path.insert(1, './graph/')
from graph import Graph
from util import Queue

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
loop_members = set()

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

'''instantiate each room as a graph vertex for bfs loop detection'''
maize = Graph()
for r in directory:
    maize.add_vertex(r)

'''creation of the edges'''
for r in directory:
    for n in directory[r][1]:
        maize.add_edge(r, n, bidir=True)

'''finds loops'''
def loopy(fork):
    for n in maize.get_neighbors(fork):
        if n in loop_members or n in leaves:
            continue
        q = Queue()
        q.enqueue([(n, fork)])
        visited = set()
        while q.size() > 0:
            path = q.dequeue()
            v = path[-1][0]
            if v not in visited:
                if v == fork:
                    for r in path:
                        loop_members.add(r[0])
                visited.add(v)
                for neighb in maize.get_neighbors(v):
                    if neighb != path[-1][1]:
                        path_copy = list(path)
                        path_copy.append((neighb, v))
                        q.enqueue(path_copy)

'''forloop to find every loop in the maize'''
for fork in forks:
    loopy(fork)

print(len(loop_members))