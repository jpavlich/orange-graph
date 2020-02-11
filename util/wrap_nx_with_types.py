import networkx as nx
import util.nx_extract as nxe
from inspect import getmembers, isfunction, signature
from util.nx_extract import get_member_metadata, FunctionMetadata
from typing import *
from jinja2 import Template, Environment

# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True


env = Environment(trim_blocks=True, lstrip_blocks=True)


def load_template(filename):
    with open(filename) as f:
        return env.from_string(f.read())


def wrap_function(fun_md: FunctionMetadata):
    pass


def process_member(m):
    fun: FunctionMetadata = get_member_metadata(m)
    if fun:
        typed_params = []
        for param in fun.signature.values():
            typed_params.append(f"${param.name}: ${param.type}")
        print(
            fun_template.render(
                fun=fun, typed_params=typed_params, len=len, iter=iter, next=next
            )
        )


if __name__ == "__main__":

    types: Set = set({})
    fun_template = load_template("util/wrapped_fun.py.j2")
    for m in getmembers(nx):
        process_member(m)
    # process_member(getmembers(nx)[-10])
