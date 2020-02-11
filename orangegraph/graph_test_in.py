import sys
import numpy
import networkx as nx
from networkx.algorithms.approximation.clique import max_clique
import Orange.data
from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets.widget import OWWidget


class GraphTestIn(OWWidget):
    name = "Graph Test In"
    description = "Test In"
    icon = "icons/graph.svg"
    priority = 10

    class Inputs:
        data = Input("data", object)

    class Outputs:
        pass

    want_main_area = False

    def __init__(self):
        super().__init__()

        # GUI
        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(
            box, "No data on input yet, waiting to get something."
        )
        self.infob = gui.widgetLabel(box, "")

    @Inputs.data
    def set_data(self, d: object):
        self.d = d

    def handleNewSignals(self):
        """Coalescing update."""
        self.commit()

    def commit(self):
        """Commit/send the outputs"""
        if self.d is not None:
            # mclique: set = max_clique(self.G)
            mclique = ""
            self.infoa.setText("Data: ")
            self.infob.setText(f"{self.d}")

        else:
            self.infoa.setText("No data on input yet, waiting to get something.")
            self.infob.setText("")

