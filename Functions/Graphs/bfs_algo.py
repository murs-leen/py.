from collections import deque


def bfs(start, graph):

    visited = set([start])  
    queue = deque([start])

    while queue:
        node = queue.popleft()
        print(node, end=" ")

        for neighbour in graph.get(node, []):

            if neighbour not in visited:
                visited.add(neighbour) 
                queue.append(neighbour)


graph = {
    'A': ['B','C'],
    'B': ['D','E'],
    'C': ['F','G'],
    'D': ['H'],
    'E': ['H'],
    'F': ['H'],
    'G': ['H'],
    'H': []
}

bfs('A', graph)
