import sys
import numpy
import networkx as nx
from networkx.algorithms.approximation.clique import max_clique
import Orange.data
from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets.widget import OWWidget
from orangegraph.functions.visualization import visualize_graph

html = """
        <p>test123</p>
"""


class GraphView(OWWidget):
    name = "Graph View"
    description = "Visualizes a graph"
    icon = "icons/graph.svg"
    priority = 10

    class Inputs:
        graph = Input("G", nx.Graph)

    want_main_area = False

    @Inputs.graph
    def set_graph(self, G):
        self.G = G

    def __init__(self):
        super().__init__()

        # GUI
        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(
            box, "No data on input yet, waiting to get something."
        )
        self.infob = gui.widgetLabel(box, "")
        gui.button(box, self, "Display", callback=self.commit)

    def commit(self):
        visualize_graph(self.G)

