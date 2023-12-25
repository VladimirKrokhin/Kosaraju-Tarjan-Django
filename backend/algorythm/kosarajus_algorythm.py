
from collections import defaultdict

def kosaraju_algo(adj_list, ids_array):
    def fill_order(v, adj_list, visited, stack):
        visited[v] = True
        for i in adj_list[v]:
            if not visited[i]:
                fill_order(i, adj_list, visited, stack)
        stack.append(v)

    def get_transpose(adj_list):
        transposed_graph = defaultdict(list)
        for i in adj_list:
            for j in adj_list[i]:
                transposed_graph[j].append(i)
        return transposed_graph

    def dfs(v, adj_list, visited, res):
        visited[v] = True
        res.append(v)
        for i in adj_list[v]:
            if not visited[i]:
                dfs(i, adj_list, visited, res)

    stack = []
    visited = {id: False for id in ids_array}
    for i in ids_array:
        if not visited[i]:
            fill_order(i, adj_list, visited, stack)
    transposed_graph = get_transpose(adj_list)
    visited = {id: False for id in ids_array}
    result = []
    while stack:
        i = stack.pop()
        if not visited[i]:
            res = []
            dfs(i, transposed_graph, visited, res)
            result.append(res)
    return result
