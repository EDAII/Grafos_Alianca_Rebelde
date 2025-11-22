from collections import deque

def bfs_levels(graph, start):
    """
    Executa BFS em um grafo não ponderado.

    """
    visited = set()
    level = {}
    order = []

    queue = deque()
    visited.add(start)
    level[start] = 0
    queue.append(start)

    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph.get(u, []):
            if v not in visited:
                visited.add(v)
                level[v] = level[u] + 1
                queue.append(v)

    return order, level


if __name__ == "__main__":
    # Exemplo rápido de uso
    graph_example = {
        "Base": ["A", "B"],
        "A": ["Base", "C", "D"],
        "B": ["Base", "E"],
        "C": ["A"],
        "D": ["A", "F"],
        "E": ["B", "F"],
        "F": ["D", "E"]
    }

    ordem, niveis = bfs_levels(graph_example, "Base")
    print("Ordem de visita:", ordem)
    print("Níveis:", niveis)
