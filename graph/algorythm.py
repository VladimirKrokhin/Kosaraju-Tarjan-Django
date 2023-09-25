from graph.model import Graph


def get_strongly_connected_component(graph: Graph, algorythm : str):
    if algorythm.lower() == "kosaraju":
        return call_kosaraju_algorythm(graph)
    elif algorythm.lower() == "tarjan":
        return call_tarjan_algorythm(graph)





def call_kosaraju_algorythm(graph: Graph):
    pass

def call_tarjan_algorythm(graph: Graph):
    pass