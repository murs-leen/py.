
def dls(node, graph, max_limit):

    visited = set()

    def dfs(node, depth):

        if depth > max_limit:
            return None
        
        visited.add(node)
        print(node , end= " -> ")
        for neighbours in graph[node]:

            if neighbours not in visited:
                dfs(neighbours, depth + 1)

    dfs(node,0)


graph = {
    'A' : ['B','C'],
    'B' : ['D','E'],
    'C' : ['F','G'],
    'D' : ['H'],
    'E' : ['H'],
    'F' : ['H'],
    'G' : ['H'],
    'H' : []
}

dls('A',graph, 3)