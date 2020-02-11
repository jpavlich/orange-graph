import networkx as nx
from inspect import getmembers, isfunction, getargspec, signature, Signature, Parameter
from docstring_parser import parse
import re
from typing import *  # Tuple, Dict, List, Any, Type, Set
from types import *
from numbers import *
import numpy as np
import io
import sys
from util.template import load_template
from jinja2 import Template


class Param(object):
    def __init__(self, name, default=None, type=None):
        super().__init__()
        self.name = name
        self.default = default
        self.type = type


def is_union(t):
    return type(t) is type(Union)


def wrap_function(name, fun: Callable):
    sig: Signature = signature(fun)
    t = load_template("./util/owwidget_wrapper.py.j2")
    params = []
    for param in sig.parameters.values():
        # print(param.name, param.annotation, param.default)
        p = Param(param.name)
        if is_union(param.annotation):
            p.type = load_template("./util/union.j2").render(param=param)
        else:
            p.type = param.annotation.__name__
        params.append(p)
    print(t.render(sig=sig, name=name, params=params))


if __name__ == "__main__":
    from orangegraph.graph_functions import *

    wrap_function("dpath", dpath)
