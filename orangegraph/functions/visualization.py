import networkx as nx
import json
import webview
from util.template import load_template
import webbrowser
from orangegraph.functions.read_write import to_dict
import random as r


def script(src):
    with open(src) as s:
        return s.read()


def visualize_graph(G):
    for e in G.edges:
        G.edges[e]["id"] = str((e[0], e[1]))

    for n in G.nodes:
        if not "x" in G.nodes[n] or not "y" in G.nodes[n]:
            G.nodes[n]["x"] = r.randint(0, 100)
            G.nodes[n]["y"] = r.randint(0, 100)

    graph_dict = to_dict(G)
    graph_json = json.dumps(graph_dict, indent=4)

    t = load_template("sandbox/graph.html.j2")
    html = t.render(graph=graph_json, script=script)
    with open("tmp/webview.html", "w") as w:
        w.write(html)
        webbrowser.open_new("tmp/webview.html")
