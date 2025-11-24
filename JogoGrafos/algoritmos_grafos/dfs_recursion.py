def dfs_recursive(graph, start_node, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    visited.add(start_node)
    path.append(start_node)

    for neighbor in graph.get(start_node, []):
        if neighbor not in visited:
            # O ponto onde a recursão acontece
            visited, path = dfs_recursive(graph, neighbor, visited, path)

    return visited, path

def get_dfs_path(graph, start_node):
    visited, path = dfs_recursive(graph, start_node)
    return visited, path