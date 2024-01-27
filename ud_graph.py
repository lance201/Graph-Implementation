# Course: CS261 Data Structures
# Author: Lok Wai Wong
# Assignment: 6
# Description: Implementing undirected graphs

from collections import deque

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        if v in self.adj_list.keys():
            return
        self.adj_list[v] = []
        
    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        if u == v:
            return
        elif v not in self.adj_list.keys() and u not in self.adj_list.keys():
            self.add_vertex(u)
            self.adj_list[u].append(v)
            self.add_vertex(v)
            self.adj_list[v].append(u)
        elif u not in self.adj_list.keys():
            self.add_vertex(u)
            self.adj_list[u].append(v)
            if v in self.adj_list.keys():
                self.adj_list[v].append(u)
        elif v not in self.adj_list.keys():
            self.add_vertex(v)
            self.adj_list[v].append(u)
            if u in self.adj_list.keys():
                self.adj_list[u].append(v)
        elif v in self.adj_list[u]:
            return
        elif u in self.adj_list[v]:
            return
        else:
            self.adj_list[v].append(u)
            self.adj_list[u].append(v)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        if u not in self.adj_list.keys():
            return
        elif v not in self.adj_list.keys():
            return
        elif u not in self.adj_list[v]:
            return
        elif v not in self.adj_list[u]:
            return
        else:
            self.adj_list[v].remove(u)
            self.adj_list[u].remove(v)

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        if v not in self.adj_list.keys():
            return
        else:
            self.adj_list.pop(v)
            for lists in self.adj_list:
                if v in self.adj_list[lists]:
                    self.adj_list[lists].remove(v)

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        return list(self.adj_list.keys())

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        edge_list = []
        for lists in self.adj_list:
            for elements in self.adj_list[lists]:
                edge_list.append(sorted((lists, elements)))
        temp_list = []
        [temp_list.append(edges) for edges in edge_list if edges not in temp_list]
        final_list = []
        [final_list.append(tuple(edges)) for edges in temp_list]

        return final_list

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        if not path:
            return True
        else:
            for index in range(len(path)):
                if path[index] not in self.adj_list.keys():
                    return False
                if index + 1 < len(path) and path[index + 1] not in self.adj_list[path[index]]:
                    return False
            return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        if v_start not in self.adj_list.keys():
            return []

        visited = []
        stack = [v_start]

        while stack:
            vertex = stack.pop()

            if vertex not in visited:
                visited.append(vertex)
                if vertex == v_end:
                    return visited
                for v in sorted(self.adj_list[vertex], reverse=True):
                    stack.append(v)

        return visited
       

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        if v_start not in self.adj_list.keys():
            return []

        visited = []
        queue = [v_start]

        while queue:
            vertex = queue.pop(0)

            if vertex not in visited:
                visited.append(vertex)
            if vertex == v_end:
                return visited
            for v in sorted(self.adj_list[vertex]):
                if v not in visited:
                    queue.append(v)

        return visited

    def count_connected_components(self):
        """
        Return number of connected components in the graph
        """
        vertex_list = []
        vertex = list(self.adj_list.keys())
        for index in range(len(vertex)):
            sorted_list = sorted(self.dfs(vertex[index]))
            if sorted_list not in vertex_list:
                vertex_list.append(sorted_list)

        return len(vertex_list)

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """

        vertices = len(self.get_vertices())
        edges = len(self.get_edges())
        components = self.count_connected_components()
        if components < 2:
            if edges >= vertices:
                return True
            else:
                return False
        else:
            vertex_list = []
            vertex = list(self.adj_list.keys())
            for index in range(len(vertex)):
                sorted_list = sorted(self.dfs(vertex[index]))
                if sorted_list not in vertex_list:
                    vertex_list.append(sorted_list)
            for comp in vertex_list:
                edge_list = []
                for elements in comp:
                    for edges in self.adj_list[elements]:
                        edge_list.append(sorted((elements, edges)))
                temp_list = []
                [temp_list.append(edges) for edges in edge_list if edges not in temp_list]
                final_list = []
                [final_list.append(tuple(edges)) for edges in temp_list]
                if len(final_list) >= len(comp):
                    return True
            return False


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
