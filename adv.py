from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# import sys
# sys.path.insert(1, "./graph/")
# from graph import Graph

from util import Stack, Queue  # These may come in handy

class Graph:
    """Represent a graph as a dictionary of vertices mapping labels to edges."""

    def __init__(self):
        self.vertices = {}
        self.cardinal_pairs = {'n':'s', 's':'n', 'e':'w', 'w':'e'}

    def add_vertex(self, vertex_id):
        self.vertices[vertex_id] = {}

    def add_edge(self, v1, v2, bidir=False):
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
            if bidir == True:
                self.vertices[v2].add(v1)
        else:
            raise IndexError('nonexistant vertex')
    
    def new_door(self, vertex_id, dirxn, destination_vertex = '?'):
        self.vertices[vertex_id][dirxn] = destination_vertex

    def get_neighbors(self, vertex_id):
        unopened = []
        doors = self.vertices[vertex_id]
        for dirxn, door in doors.items():
            if door == '?':
                unopened.append(dirxn)
        return unopened

    def bft(self, starting_vertex):
        q = Queue()
        visited = []
        q.enqueue(starting_vertex)
        while q.size() > 0:
            v = q.dequeue()
            if v not in visited:
                visited.append(v)
                for vert in self.get_neighbors(v):
                    q.enqueue(vert)
        return visited

    def dft(self, dirxn = None, prev = None):
        # s = Stack()
        # visited = []
        # s.push(starting_vertex)
        # while s.size() > 0:
        #     v = s.pop()
        #     if v not in visited:
        #         visited.append(v)
        #         for vert in self.get_neighbors(v):
        #             s.push(vert)
        # return visited
        if dirxn:
            player.travel(dirxn)
            traversal_path.append(dirxn)

        cur = player.current_room

        if cur.id not in self.vertices:
            self.add_room(cur.id)
            doors = cur.get_exits()
            for door in doors:
                self.new_door(cur.id, door)
        
        if prev:
            self.new_door(prev.id, dirxn, cur.id)
            self.new_door(cur.id, self.cardinal_pairs[dirxn], prev.id)
        
        if len(self.vertices) == len(room_graph):
            return
        
        untraversed = self.get_neighbors(cur.id)

        if len(untraversed) > 0:
            for room in untraversed:
                self.dft(room, cur)
        
        else:
            unvisited_path = self.bfs(cur)
            if not unvisited_path:
                return
            crow_flies = list(map(lambda x: x[1], unvisited_path))
            traversal_path.extend(crow_flies)
            for move in crow_flies:
                player.travel(move)
            self.dft()

    def dft_recursive(self, start_vert, vis=set()):
        if start_vert not in vis:
            print(start_vert)
            vis.add(start_vert)
            for n in self.get_neighbors(start_vert):
                self.dft_recursive(n, vis=vis)

    def bfs(self, starting_vertex): # , destination_vertex
        q = Queue()
        q.enqueue([(starting_vertex.id, None)])
        visited = set()
        while q.size() > 0:
            path = q.dequeue()
            v = path[-1][0]
            unseen = self.get_neighbors(v)
            # if v not in visited:
            #     if v == destination_vertex:
            #         return path
            #     visited.add(v)
            #     for next_v in self.get_neighbors(v):
            #         path_copy = list(path)
            #         path_copy.append(next_v)
            #         q.enqueue(path_copy)
            if len(unseen) > 0:
                return path[1:]
            for dirxn, room in self.vertices[v].items():
                q.enqueue(path + [(room, dirxn)])
        return None

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
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

maze_graph = Graph()
maze_graph.dft()

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
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
