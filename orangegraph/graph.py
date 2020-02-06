import sys
import numpy
import networkx as nx
import Orange.data
from Orange.widgets import widget, gui
from Orange.widgets.utils.signals import Input, Output


class Graph(widget.OWWidget):
    name = "Graph"
    description = "Represents a graph in memory"
    icon = "icons/graph.svg"
    priority = 10

    class Inputs:
        edges = Input("Edges", Orange.data.Table)

    class Outputs:
        graph = Output("Graph", nx.Graph)

    want_main_area = False

    def __init__(self):
        super().__init__()

        # GUI
        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(
            box, "No data on input yet, waiting to get something."
        )
        self.infob = gui.widgetLabel(box, "")

    @Inputs.edges
    def set_edges(self, dataset):
        if dataset is not None:
            G: nx.Graph = nx.Graph()
            for row in dataset:
                G.add_edge(row["source"], row["target"])
            self.infoa.setText("Graph")
            self.infob.setText(
                f"Nodes: {G.number_of_nodes()}. Edges: {G.number_of_edges()}"
            )
            self.Outputs.graph.send(G)
        else:
            self.infoa.setText("No data on input yet, waiting to get something.")
            self.infob.setText("")
            self.Outputs.graph.send(None)
