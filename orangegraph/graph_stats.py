import sys
import numpy
import networkx as nx
import Orange.data
from Orange.widgets import widget, gui
from Orange.widgets.utils.signals import Input, Output


class GraphStats(widget.OWWidget):
    name = "Graph Stats"
    description = "Calculates some graph stats"
    icon = "icons/graph.svg"
    priority = 10

    class Inputs:
        edges = Input("Graph", nx.Graph)

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
    def set_graph(self, G: nx.Graph):
        if G is not None:
            self.infoa.setText("Graph stats")
            self.infob.setText(
                f"Nodes: {G.number_of_nodes()}. Edges: {G.number_of_edges()}"
            )
            self.Outputs.graph.send(G)
        else:
            self.infoa.setText("No data on input yet, waiting to get something.")
            self.infob.setText("")
            self.Outputs.graph.send(None)
