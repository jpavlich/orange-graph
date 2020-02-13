import sys
import numpy
import networkx as nx
import Orange.data
from Orange.widgets import widget, gui
from Orange.widgets.utils.signals import Input, Output
from orangegraph.functions.read_write import to_dict


class GraphToDict(widget.OWWidget):
    name = "To Dict"
    description = "Converts a graph into a dictionary"
    icon = "icons/graph.svg"
    priority = 10

    class Inputs:
        in_graph = Input("Graph", nx.Graph)

    class Outputs:
        out_dict = Output("Dict", dict)

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
            d = to_dict(self.G)
            print(d)
            self.Outputs.out_dict.send(d)
        else:
            self.infoa.setText("No data on input yet, waiting to get something.")
            self.infob.setText("")
            self.Outputs.out_graph.send(None)

