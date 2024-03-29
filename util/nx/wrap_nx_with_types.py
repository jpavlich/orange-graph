import networkx as nx
import util.nx_extract as nxe
from inspect import getmembers, isfunction, signature
from util.nx_extract import get_member_metadata, FunctionMetadata
from typing import *
from util.template import load_template


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
    for i, m in enumerate(getmembers(nx)):
        print(f"#{i}")
        process_member(m)
    # process_member(getmembers(nx)[716])
