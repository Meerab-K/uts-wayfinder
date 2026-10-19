# Import libraries
import heapq
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Load the data
folder = Path(__file__).resolve().parent.parent
df_buildings = pd.read_csv(folder / "data" / "nodes.csv")
df_matrix = pd.read_csv(folder / "data" / "adjacency_matrix.csv")


# Create a dictionary of buildings with their coordinates
buildings = {}

name = df_buildings["LocationName"]
locationX = df_buildings["LocationX"]
locationY = df_buildings["LocationY"]

location = zip(locationX, locationY)

for x1,x2 in zip(name, location):
    buildings.update({x1:x2})


# Create a list of neighbours based on the adjacency matrix
neighbours=[]

for i in range (df_matrix.shape[0]):
    x = df_matrix.iloc[i,:]
    relationKey=(x.iloc[0])

    for j in range (1, df_matrix.shape[1]):
        if (j>i and x.iloc[j] != 0 ):
            temp_tuple = (relationKey, df_matrix.columns[j], int(x.iloc[j]))
            neighbours.append(temp_tuple)


# function to calculate the heuristic between two nodes (locations)
def heuristic(u, v):
    return np.sqrt(sum((x - y) ** 2 for x, y in zip(buildings[u], buildings[v])))


# Define priority queue class for managing nodes based on priority
class PriorityQueue:
    def __init__(self):
        self._heap = []

    def push(self, item, priority):
        heapq.heappush(self._heap, (priority, item))

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from an empty priority queue")
        return heapq.heappop(self._heap)[1]

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from an empty priority queue")
        return self._heap[0][1]

    def is_empty(self):
        return len(self._heap) == 0

    def __len__(self):
        return len(self._heap)

    def returnItems(self):
        return [item for _, item in self._heap]

    def returnElements(self):
        return [(int(priorityValue),item) for priorityValue, item in self._heap]


# A* search algorithm implementation using the PriorityQueue class
def my_astar_path(G, start, goal):
    # Check the start node
    print('start node: {}'.format(start))

    # Initialise a priority queue object to be the frontier -- an empty priority list
    pq = PriorityQueue()

    # Initialise the frontier by the start location and its path
    pq.push((start,[start]),0+heuristic(start,goal))

    # initialise the explored set to be an empty set
    visited = set()

    index = 0
    while pq:
        print('Iteration {}'.format(index))

        (vertex, path) = pq.pop()
        index = index +1

        if vertex in visited:
            continue
        visited.add(vertex)

        if vertex == goal:  #late goal check
            return path, index
        
        for neighbor in G[vertex]:
            if neighbor in visited:
                continue
            pq.push((neighbor, path + [neighbor]), nx.path_weight(G, path + [neighbor],'weight')+heuristic(neighbor,goal))

    return None, index  # Return None if no path is found

# Function to generate image of the map with the path highlighted
def generate_map_path(G, path):
    map_image = plt.imread(folder / "img" / "Map.png")

    pos = {node: buildings[node] for node in path}
    path_edges = list(zip(path[:-1], path[1:]))

    fig, ax = plt.subplots(figsize=(140, 90))

    ax.imshow(map_image, extent=[0, 100, 0, 100])

    nx.draw_networkx_nodes(
        G, pos, nodelist=path, ax=ax
    )
    
    nx.draw_networkx_edges(
        G, pos, edgelist=path_edges,
        edge_color="red", width=3, ax=ax
    )

    nx.draw_networkx_labels(
        G, pos, labels={node: node for node in path}, ax=ax, font_size=8
    )

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    return fig