import sys
import numpy
import networkx as nx
from networkx.algorithms.approximation.clique import max_clique
import Orange.data
from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets.widget import OWWidget


class GraphAlgorithm(OWWidget):
    name = "Graph Algorithm"
    description = "Applies algorithm over a graph"
    icon = "icons/graph.svg"
    priority = 10

    class Inputs:
        in_graph = Input("Graph", nx.Graph)

    class Outputs:
        result = Output("Result", Orange.data.Table)

    want_main_area = False

    def __init__(self):
        super().__init__()

        # GUI
        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(
            box, "No data on input yet, waiting to get something."
        )
        self.infob = gui.widgetLabel(box, "")

        gui.button(box, self, "Commit", callback=self.commit)

    @Inputs.in_graph
    def set_in_graph(self, G: nx.Graph):
        self.G = G

    # def handleNewSignals(self):
    #     """Coalescing update."""
    #     self.commit()

    def commit(self):
        """Commit/send the outputs"""
        if self.G is not None:
            mclique: set = max_clique(self.G)
            self.infoa.setText("Max clique:")
            self.infob.setText(f"Nodes: {len(mclique)}")
            self.Outputs.result.send(None)
        else:
            self.infoa.setText("No data on input yet, waiting to get something.")
            self.infob.setText("")
            self.Outputs.result.send(None)

