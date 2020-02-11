import sys
import numpy
import networkx as nx
from networkx.algorithms.approximation.clique import max_clique
import Orange.data
from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets.widget import OWWidget


class GraphTestOut(OWWidget):
    name = "Graph Test Out"
    description = "Test Out"
    icon = "icons/graph.svg"
    priority = 10

    class Inputs:
        pass

    class Outputs:
        result = Output("data", object)

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

    def commit(self):
        """Commit/send the outputs"""
        self.Outputs.result.send("aaaa")

