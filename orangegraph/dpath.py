import sys
import numpy
import networkx
from networkx.algorithms.approximation.clique import max_clique
import Orange.data
from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets.widget import OWWidget


class dpath(OWWidget):
    name = "dpath"
    description = "Applies algorithm over a graph"
    icon = "icons/graph.svg"
    priority = 10

    class Inputs:
        G = Input("G", networkx.classes.graph.Graph)
        source = Input("source", object)
        target = Input("target", object)
        weight = Input("weight", str)
        

    class Outputs:
        result = Output("Result", Orange.data.table.Table)

    want_main_area = False

    def __init__(self):
        super().__init__()

        # GUI
        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(
            box, "No data on input yet, waiting to get something."
        )
        self.infob = gui.widgetLabel(box, "")


        self.txt_source = gui.lineEdit(box, self, '', orientation="horizontal", label="source:")
        self.txt_source.textChanged.connect(self.update_source)


        self.txt_target = gui.lineEdit(box, self, '', orientation="horizontal", label="target:")
        self.txt_target.textChanged.connect(self.update_target)


        self.txt_weight = gui.lineEdit(box, self, '', orientation="horizontal", label="weight:")
        self.txt_weight.textChanged.connect(self.update_weight)


        gui.button(box, self, "Commit", callback=self.commit)


    def update_G(self):
        try:
            G_value = eval(self.txt_G.text())
            self.G = G_value

        except:
            pass



    def update_source(self):
        try:
            source_value = eval(self.txt_source.text())
            self.source = source_value

        except:
            pass



    def update_target(self):
        try:
            target_value = eval(self.txt_target.text())
            self.target = target_value

        except:
            pass



    def update_weight(self):
        try:
            weight_value = eval(self.txt_weight.text())
            self.weight = weight_value

        except:
            pass



    @Inputs.G
    def set_G(self, G: networkx.classes.graph.Graph):
        self.G = G

    @Inputs.source
    def set_source(self, source: object):
        self.source = source

    @Inputs.target
    def set_target(self, target: object):
        self.target = target

    @Inputs.weight
    def set_weight(self, weight: str):
        self.weight = weight
    

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
