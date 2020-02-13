import sys
import numpy
import networkx as nx
import Orange.data
from Orange.widgets import gui
from Orange.widgets.widget import OWWidget, Msg
from Orange.widgets.utils.signals import Input, Output


class Graph(OWWidget):
    name = "Graph"
    description = "Represents a graph in memory"
    icon = "icons/graph.svg"
    priority = 10

    class Inputs:
        nodes = Input("Nodes", Orange.data.Table)
        edges = Input("Edges", Orange.data.Table)

    class Outputs:
        graph = Output("G", nx.Graph)

    want_main_area = False

    def __init__(self):
        super().__init__()

        # GUI
        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(
            box, "No data on input yet, waiting to get something."
        )
        self.infob = gui.widgetLabel(box, "")

    @Inputs.nodes
    def set_nodes(self, nodes):
        self.nodes = nodes

    @Inputs.edges
    def set_edges(self, edges):
        self.edges = edges

    def handleNewSignals(self):
        """Coalescing update."""
        self.commit()

    class Error(OWWidget.Error):
        wrong_input = Msg("Wrong input: {message}")

    def commit(self):
        try:
            G: nx.Graph = nx.Graph()
            if self.nodes is not None:
                for row in self.nodes:
                    print(row)
                    G.add_node(row["id"])

            if self.edges is not None:
                for row in self.edges:
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
        except ValueError as e:
            self.Error.wrong_input(message=str(e))
