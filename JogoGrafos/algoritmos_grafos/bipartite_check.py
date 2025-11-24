from collections import deque

def is_bipartite_check(graph, start_node):

    colors = {node: 0 for node in graph}
    queue = deque([start_node])
    colors[start_node] = 1 
    all_nodes = set(graph.keys())

    while queue:
        u = queue.popleft()
        current_color = colors[u]
        next_color = 2 if current_color == 1 else 1

        for v in graph.get(u, []):
            if colors[v] == 0:
                colors[v] = next_color
                queue.append(v)
            elif colors[v] == current_color:
                return False, colors, f"Conflito: Planeta {v} ligado a {u} tem a mesma cor."

    # Se a BFS terminou e todos os nós alcançados foram coloridos sem conflito, é bipartido
    if len(colors) == len(all_nodes):
        return True, colors, "Sucesso: O grafo é bipartido (2-colorível)."
    else:

        return True, colors, "A aliança é bipartida, mas o grafo é desconexo."