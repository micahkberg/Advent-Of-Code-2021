from load import openfile
import itertools
import queue

today = "Day15"
lines = openfile(today+".txt")
#print(lines)
print("Read txt...")
cave = []
for line in lines:
    cave.append(list(map(int, line)))

vertex_coords = itertools.product(range(100),range(100))
vertex_graph = {}
neighbor_dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
for vertex in vertex_coords:
    vertex_graph[vertex] = {}
    for neighbor in neighbor_dirs:
        if vertex[0]+neighbor[0] in range(100) and vertex[1]+neighbor[1] in range(100) and neighbor != (0, 0):
            vertex_graph[vertex][(vertex[0]+neighbor[0],
                                  vertex[1]+neighbor[1])] = cave[vertex[1]+neighbor[1]][vertex[0]+neighbor[0]]
print("Built vertex graph....")
small_map_max = sum(list(map(sum, cave)))


class Graph:
    def __init__(self, vertices):
        self.v = vertices
        self.v_len = len(vertices)
        self.visited = []


def dijkstra(graph, start_vertex):
    D = {v:small_map_max for v in graph.v}
    D[start_vertex] = 0
    pq = queue.PriorityQueue()
    pq.put((0, start_vertex))
    while not pq.empty():
        (dist, current_vertex) = pq.get()
        graph.visited.append(current_vertex)
        for neighbor in vertex_graph[current_vertex].keys():
            distance = vertex_graph[current_vertex][neighbor]
            if neighbor: #not in graph.visited:
                old_cost = D[neighbor]
                new_cost = D[current_vertex] + distance
                if new_cost < old_cost:
                    pq.put((new_cost, neighbor))
                    D[neighbor] = new_cost
    return D


c = Graph(vertex_graph.keys())
print("Initialized graph obj...")
print("Beginning algo...")
results = dijkstra(c, (0,0))
print("Answer 1 found")
print(results[(99,99)])
print("starting part 2")

# part 2

big_coords = list(itertools.product(range(500),range(500)))
big_map_max = (small_map_max * 25) + (9*500**2)
print("made coord list...")
c2 = Graph(big_coords)
print("made graph")

def get_neighbors(coord):
    neighbors = []
    for n in neighbor_dirs:
        x = n[0]+coord[0]
        y = n[1]+coord[1]
        if x in range(500) and y in range(500):
            neighbors.append((x,y))
    return neighbors

def get_weight(d): #d for destination
    val = cave[d[1]%100][d[0]%100]
    val += d[1]//100 + d[0]//100
    if val>9:
        val-=9
    return val

def big_dijkstra(graph, start_vertex):
    D = {v:big_map_max for v in graph.v}
    print("initialized D dict")
    D[start_vertex] = 0
    pq = queue.PriorityQueue()
    pq.put((0, start_vertex))
    print("initialized queue, beginning algorithm in earnest")
    while not pq.empty():
        (dist, current_vertex) = pq.get()
        graph.visited.append(current_vertex)
        if (len(graph.visited)/(500*500)) in map(lambda i: i/100.0, range(100)):
            print(len(graph.visited)/(500*500))

        for neighbor in get_neighbors(current_vertex):
            distance = get_weight(neighbor)
            old_cost = D[neighbor]
            new_cost = D[current_vertex] + distance
            if new_cost < old_cost:
                pq.put((new_cost, neighbor))
                D[neighbor] = new_cost
    return D



results2 = big_dijkstra(c2, (0,0))
print(results2[(499,499)])
