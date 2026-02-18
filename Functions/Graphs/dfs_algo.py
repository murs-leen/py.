
        # ---DFS (Recursive) ----


def dfs(start, visited, graph):

    visited.append(start)
    print(start,end=" -> ")

    for neighbour in graph[start]:

        if neighbour not in visited:
            dfs(neighbour,visited, graph)


        # ------DFS (stack) ------


def dfs_traversal(graph, start):

    print("\n---------DFS using stack-----------\n")
    
    visited = set()
    stack = [start]   # stack (LIFO)

    while stack:

        node = stack.pop()  # pop from the end (top of stack)
        visited.add(node)
        print(node,end=" -> ")

        # Add neighbors to stack
        # Reverse to keep a similar left-to-right order as recursive DFS (optional)

        for neighbor in reversed(graph.get(node, [])):

            if neighbor not in visited:
                stack.append(neighbor)

    
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

visited = []
print("\n---------DFS recursive-----------\n")
dfs('A',visited, graph)
dfs_traversal(graph, 'A')
