import networkx as nx


def to_dict(G):
    data = nx.readwrite.json_graph.node_link_data(G)
    data["edges"] = data["links"]
    del data["links"]
    return data
