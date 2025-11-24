from collections import deque

def _bfs_check(graph, start_node):
    queue = deque([start_node])
    visited = {start_node}
    
    while queue:
        u = queue.popleft()
        for v in graph.get(u, []):
            if v not in visited:
                visited.add(v)
                queue.append(v)
    
    return visited

def get_transposed_graph(graph):
    transposed = {node: [] for node in graph}
    for u, neighbors in graph.items():
        for v in neighbors:
            transposed[v].append(u)
    return transposed

def is_strongly_connected_component(graph, start_node):
    
    all_nodes = set(graph.keys())
    
    visited_original = _bfs_check(graph, start_node)
    
    transposed_graph = get_transposed_graph(graph)
    
    visited_transposed = _bfs_check(transposed_graph, start_node)

    is_scc = (visited_original == all_nodes) and (visited_transposed == all_nodes)
    
    return is_scc, visited_original, visited_transposed