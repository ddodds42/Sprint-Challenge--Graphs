from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

import sys
sys.path.insert(1, './graph/')
from graph import Graph
from util import Queue, Stack

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

'''this loop populates each rooms dict in directory with the swapped values.
{0: [(3, 5), {'n': 1, 's': 5, 'e': 3, 'w': 7}]}
becomes
{0: [(3, 5), {1:'n', 5:'s', 3:'e', 7:'w'}]}
'''
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

'''custom dft to return members of a single branch'''
def dft_custom(current, prev):
    s = Stack()
    visited = [prev]
    s.push(current)
    while s.size() > 0:
        v = s.pop()
        if v not in visited:
            visited.append(v)
            for vert in maize.get_neighbors(v):
                s.push(vert)
    return visited

'''let's start traversing! First branch, then loop.'''

'''
THE FXN BELOW IS NOT RETURNING A CORRECT BACKTACKED TRAVERSAL OF A BRANCH.
YOU NEED TO
1] GET THAT RUNNING CORRECTLY FOR BRANCHES WITHOUT ROOM LOOPS, THEN
2] GET IT OR ANOTHER FXN WORKING CORRECTLY FOR BRANCHES IN BETWEEN LOOPS, THEN
3] STITCH TOGETHER THE ABOVE FXNS INTO THE TRAVERSER FXN FROM PSEUDOPAD.TXT
'''
branchtest = dft_custom(105, 104)

print(branchtest)

def dft_path(dft_list):
    s = Stack()
    visited = [dft_list[0]]
    s.push((dft_list[1], dft_list[0]))
    while s.size() > 0:
        v = s.pop()
        if v[0] in leaves:
                visited += maize.bfs(v[0], s.stack[-1][0])
                v = s.pop()
                for vert in maize.get_neighbors(v[0]):
                    if vert != v[1]:
                        s.push((vert, v[0]))
        elif v[0] not in visited:
            visited.append(v[0])
            for vert in maize.get_neighbors(v[0]):
                if vert != v[1]:
                    s.push((vert, v[0]))
    if visited != dft_list[1]:
        visited += maize.bfs(visited[-1],dft_list[1])[1:]
    return visited[1:]


print(dft_path(branchtest))