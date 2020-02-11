import networkx as nx
import util.nx_extract as nxe
from inspect import getmembers, isfunction, signature
from util.nx_extract import get_member_metadata, FunctionMetadata
from typing import *
from jinja2 import Template


def load_template(filename):
    with open(filename) as f:
        return Template(f.read())


def wrap_function(fun_md: FunctionMetadata):
    pass


if __name__ == "__main__":
    types: Set = set({})
    fun_template = load_template("util/wrapped_fun.py.j2")
    for m in getmembers(nx):
        md = get_member_metadata(m)
        if md:
            print(fun_template.render(fun=md))
            # for param, desc in md.signature.items():
