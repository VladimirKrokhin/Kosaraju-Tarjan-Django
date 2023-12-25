def tarjan_algo(adj_list, nodes_ids_list):
    time = 0
    discovered = {node_id: -1 for node_id in nodes_ids_list}
    lowest = {node_id: -1 for node_id in nodes_ids_list}
    in_stack = {node_id: False for node_id in nodes_ids_list}
    stack = []
    result = []

    def scc_util(node, component):
        nonlocal time
        discovered[node] = time
        lowest[node] = time
        time += 1
        in_stack[node] = True
        stack.append(node)

        for neighbor in adj_list[node]:
            if discovered[neighbor] == -1:
                scc_util(neighbor, component)
                lowest[node] = min(lowest[node], lowest[neighbor])
            elif in_stack[neighbor] == True:
                lowest[node] = min(lowest[node], discovered[neighbor])

        if lowest[node] == discovered[node]:
            temp_component = []
            while True:
                w = stack.pop()
                in_stack[w] = False
                temp_component.append(w)
                if w == node:
                    break
            component.append(temp_component)

    for node_id in nodes_ids_list:
        if discovered[node_id] == -1:
            component = []
            scc_util(node_id, component)
            if component:
                result.extend(component)

    return result
