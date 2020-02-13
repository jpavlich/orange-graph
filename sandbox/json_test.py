import networkx as nx
import json
import webview
from util.template import load_template
import webbrowser


def script(src):
    with open(src) as s:
        return s.read()


if __name__ == "__main__":

    G = nx.Graph()

    for i in range(0, 5):
        G.add_node(i, x=i * 10, y=i * 10)

    for i in range(0, 5):
        for j in range(0, 5):
            G.add_edge(i, j)

    for e in G.edges:
        G.edges[e]["id"] = str((e[0], e[1]))

    data = nx.readwrite.json_graph.node_link_data(G)
    data["edges"] = data["links"]
    del data["links"]
    graph = json.dumps(data, indent=4)

    t = load_template("sandbox/graph.html.j2")
    html = t.render(graph=graph, script=script)
    with open("tmp/webview.html", "w") as w:
        w.write(html)
        webbrowser.open_new("tmp/webview.html")
