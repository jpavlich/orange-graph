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
from util.introspect import full_name, is_primitive
import Orange.data
from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets.widget import OWWidget


class Param(object):
    def __init__(self, name, default=None, type=None):
        super().__init__()
        self.name = name
        self.default = default
        self.type = type


def wrap_type(t: Type):
    fname = full_name(t)
    if fname == "typing.List":
        return Orange.data.Table
    else:
        return t


def wrap_function(name, fun: Callable):
    sig: Signature = signature(fun)
    t = load_template("./util/templates/owwidget_wrapper.py.j2")
    params = []
    for param in sig.parameters.values():
        p = Param(param.name)
        p.type = wrap_type(param.annotation)
        params.append(p)
    ret_type = wrap_type(sig.return_annotation)
    print(
        t.render(
            sig=sig,
            name=name,
            params=params,
            ret_type=ret_type,
            full_name=full_name,
            is_primitive=is_primitive,
        )
    )


if __name__ == "__main__":
    from orangegraph.functions import *

    wrap_function("dpath", dpath)
