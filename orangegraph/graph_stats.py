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
        in_graph = Input("Graph", nx.Graph)

    class Outputs:
        out_graph = Output("Graph", nx.Graph)

    want_main_area = False

    def __init__(self):
        super().__init__()

        # GUI
        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(
            box, "No data on input yet, waiting to get something."
        )
        self.infob = gui.widgetLabel(box, "")

    @Inputs.in_graph
    def set_in_graph(self, G: nx.Graph):
        self.G = G

    def handleNewSignals(self):
        """Coalescing update."""
        self.commit()

    def commit(self):
        """Commit/send the outputs"""
        if self.G is not None:
            self.infoa.setText("Graph stats")
            self.infob.setText(
                f"Nodes: {self.G.number_of_nodes()}. Edges: {self.G.number_of_edges()}"
            )
            self.Outputs.out_graph.send(self.G)
        else:
            self.infoa.setText("No data on input yet, waiting to get something.")
            self.infob.setText("")
            self.Outputs.out_graph.send(None)

