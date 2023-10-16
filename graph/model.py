class Edge():
    def __init__(self, index: int, source: Node, destination: Node):
        self.index = index 
        self.source = source  # вершина, из которой исходит ребро
        self.destination = destination # вершина, куда исходит ребро


class Node():
    def __init__(self, index: int, inedges: list(Edge)):
        self.index = index
        self.inedges = inedges



    

class Graph():
    '''
      Посмотри здесь
      https://youtu.be/VehB3eglQMQ
    '''
    edges = list(Edge) # граф как список ребер

    def __init__(self, edge_list: list(Edge)):
        self.edges = edge_list


    # def get_node(self, value: int):
    #     if (self.is_contains_node(value)):
    #         return self.graph[value]
    #     raise Exception("Node not found!")
    

    def add_node(self, edge: Edge , index: int):
        if (self.is_contains_node(index)):
            raise Exception("Node already exists!")
        if 
        


    def is_contains_node(self, index: int):
        for edge in self.edges:
            if edge.source.index == index or edge.destination.index == index:
                return True
        return False    

    '''
    https://ru.wikipedia.org/wiki/%D0%AD%D0%B9%D0%BB%D0%B5%D1%80%D0%BE%D0%B2_%D1%86%D0%B8%D0%BA%D0%BB
    '''
    def get_indeg(self, node_index: int):
        node = self.get_node(node_index)
        return 


    def create_graph(graph_data: list[list]):  # принимает целочисленный двумерный массив
        graph = Graph()
        for row in graph_data:
            index, source, destination = [row[i] for i in range(2)]
            graph.add_node(node_value) # создает родительскую вершину (из к-рой исходит ребро)
            node = graph.get_node(node_value)
            if not graph.is_contains_node(adjacent_node_value): # проверяем, существует ли уже смежная вершина
                graph.add_node(adjacent_node_value) # добавляем смежную вершину, в которую исходит ребро из node
            adjacent_node = graph.get_node(adjacent_node)
            edge = Edge(adjacent_node)
            node.edges.add(edge)
            adjacent_node.parents[node] = edge
        return graph

