import sys
import numpy
import networkx as nx
import Orange.data
from Orange.widgets import widget, gui
from Orange.widgets.utils.signals import Input, Output
import json


class ObjToJson(widget.OWWidget):
    name = "Object to Json"
    description = "Converts an object into JSON format"
    icon = "icons/graph.svg"
    priority = 10

    class Inputs:
        in_obj = Input("Graph", object)

    class Outputs:
        out_json = Output("Json", str)

    want_main_area = False

    def __init__(self):
        super().__init__()

        # GUI
        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(
            box, "No data on input yet, waiting to get something."
        )
        self.infob = gui.widgetLabel(box, "")

    @Inputs.in_obj
    def set_in_obj(self, obj: nx.Graph):
        self.obj = obj

    def handleNewSignals(self):
        """Coalescing update."""
        self.commit()

    def commit(self):
        """Commit/send the outputs"""
        if self.obj is not None:
            j = json.dumps(self.obj, indent=4)
            print(j)
            self.Outputs.out_json.send(j)
        else:
            self.infoa.setText("No data on input yet, waiting to get something.")
            self.infob.setText("")
            self.Outputs.out_json.send(None)

