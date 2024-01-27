# Course: CS261 - Data Structures
# Author: Lok Wai Wong
# Assignment: 6
# Description: Implementing a directed weighted graph

import heapq
from collections import deque

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        This method adds a new vertex to the graph.
        """
        u = []
        if self.v_count == 0:
            self.adj_matrix.append([0])
        else:
            for index in range(self.v_count):
                self.adj_matrix[index].append(0)
            for index in range(self.v_count + 1):
                u.append(0)
            self.adj_matrix.append(u)
        self.v_count += 1
        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        This method adds a new edge to the graph.
        """
        if src == dst:
            return
        elif src > self.v_count - 1 or src < 0:
            return
        elif dst > self.v_count - 1 or dst < 0:
            return
        elif weight < 0:
            return

        self.adj_matrix[src][dst] = weight


    def remove_edge(self, src: int, dst: int) -> None:
        """
        This method removes an edge between the two vertices with provided indices.
        """
        if src == dst:
            return
        elif src > self.v_count - 1 or src < 0:
            return
        elif dst > self.v_count - 1 or dst < 0:
            return
        elif self.adj_matrix[src][dst] == 0:
            return
        else:
            self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        This method returns a list of the vertices of the graph.
        """
        vertices_list = []
        for index in range(self.v_count):
            vertices_list.append(index)
        return vertices_list

    def get_edges(self) -> []:
        """
        This method returns a list of edges in the graph.
        """
        edges_list = []
        for row in range(self.v_count):
            for col in range(self.v_count):
                if self.adj_matrix[row][col] != 0:
                    edges_list.append((row, col, self.adj_matrix[row][col]))
        return edges_list

    def is_valid_path(self, path: []) -> bool:
        """
        This method takes a list of vertex indices and returns True if
        the sequence of vertices represents a valid path in the graph.
        """
        if not path:
            return True
        else:
            for index in range(len(path)):
                if index not in self.get_vertices():
                    return False
                if index + 1 < len(path) and self.adj_matrix[path[index]][path[index + 1]] == 0:
                    return False
            return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        This method performs a depth-first search in the graph and returns a list of vertices
        visited during the search, in the order they were visited.
        """
        if v_start not in self.get_vertices():
            return []

        visited = []
        stack = [v_start]

        while stack:
            vertex = stack.pop()

            if vertex not in visited:
                visited.append(vertex)
                if vertex == v_end:
                    return visited
                linked = []
                for col in range(self.v_count):
                    if self.adj_matrix[vertex][col] != 0:
                        linked.append(col)
                for v in sorted(linked, reverse=True):
                    stack.append(v)

        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        This method performs a breadth-first search in the graph and returns a list of vertices
        visited during the search, in the order they were visited.
        """
        if v_start not in self.get_vertices():
            return []

        visited = []
        queue = [v_start]

        while queue:
            vertex = queue.pop(0)

            if vertex not in visited:
                visited.append(vertex)
            if vertex == v_end:
                return visited
            linked = []
            for col in range(self.v_count):
                if self.adj_matrix[vertex][col] != 0:
                    linked.append(col)
            for v in sorted(linked):
                if v not in visited:
                    queue.append(v)

        return visited

    def has_cycle(self):
        """
        This method returns True if there is at least one cycle in the graph, returns False otherwise.
        """

        color = ["WHITE"] * self.v_count
        for i in range(self.v_count):
            if color[i] == "WHITE":
                if self.dfs_helper(i, color):
                    return True
        return False

    def dfs_helper(self, vertex, color):
        """
        This is a helper method using colors to define whether a vertex has been visited and in a cycle.
        """
        vertex_list = self.get_vertices()
        color[vertex] = "GRAY"
        linked = []
        for col in range(self.v_count):
            if self.adj_matrix[vertex][col] != 0:
                linked.append(col)
        if not linked:
            color[vertex] = "BLACK"
            return False
        else:
            for v in linked:
                if color[v] == "GRAY":
                    return True
                if color[v] == "WHITE" and self.dfs_helper(v, color):
                    return True

        color[vertex] = "BLACK"
        return False

    def dijkstra(self, src: int) -> []:
        """
        This method implements the Dijkstra algorithm to compute the length of the shortest path from
        a given vertex to all other vertices in the graph.
        """
        visited = {}
        heap = []
        heapq.heappush(heap, (src, 0))
        while heap:
            v, dist = heapq.heappop(heap)
            if v in visited.keys() and dist < visited[v]:
                visited[v] = dist
                linked = []
                for col in range(self.v_count):
                    if self.adj_matrix[v][col] != 0:
                        linked.append((col, self.adj_matrix[v][col]))

                for vertex, dist2 in linked:
                    heapq.heappush(heap, (vertex, dist + dist2))
            if v not in visited.keys():
                visited[v] = dist
                linked = []
                for col in range(self.v_count):
                    if self.adj_matrix[v][col] != 0:
                        linked.append((col, self.adj_matrix[v][col]))

                for vertex, dist2 in linked:
                    heapq.heappush(heap, (vertex, dist + dist2))

        output = []
        for index in range(self.v_count):
            if index not in visited.keys():
                output.append(float('inf'))
            else:
                output.append(visited[index])

        return output


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
            (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # edges = [(0, 4, 6), (1, 11, 16), (3, 5, 17), (3, 6, 1), (5, 10, 11), (7, 11, 10), (9, 11, 13),
    #          (10, 3, 15), (12, 2, 1), (12, 7, 14), (12, 6, 9)]
    # edges = [(1, 3, 2), (1, 11, 11), (3, 5, 9), (3, 6, 4), (4, 2, 14), (4, 10, 8), (5, 0, 12),
    #           (5, 7, 8), (7, 4, 3), (8, 11, 20), (11, 4, 10), (12, 11, 1)]
    g = DirectedGraph(edges)
    # print('\n', g)
    # print(g.get_edges(), g.has_cycle(), sep='\n')
    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
       g.remove_edge(src, dst)
       print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
       g.add_edge(src, dst)
       print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #         (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    edges = [(0, 1, 13), (2, 5, 19), (2, 6, 2), (2, 10, 16), (3, 0, 16), (3, 9, 3), (5, 0, 1),
            (6, 3, 11), (7, 5, 14), (7, 8, 19), (9, 5, 2), (10, 9, 14), (11, 2, 7), (12, 6, 9)]

    g = DirectedGraph(edges)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
