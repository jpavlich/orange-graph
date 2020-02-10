import networkx as nx
from inspect import getmembers, isfunction, getargspec, signature, Signature, Parameter
from docstring_parser import parse
import re
from typing import *  # Tuple, Dict, List, Any, Type, Set
from types import *
from numbers import *
import numpy as np
import io

PARAMETERS = "Parameters"
RETURNS = "Returns"
SEE = "See"


def str_to_type(typename: str) -> Type:
    type_map: Dict[str, Type] = {
        "integer": int,
        "random_state": Type[Any],
        "none": Type[None],
        "graph": nx.Graph,
        "string": str,
        "file": str,
        "iterable": Iterable,
        "graph (undirected)": nx.Graph,
        "directory path": str,
        "optional": Type[None],
        "boolean": bool,
        "networkx graph": nx.Graph,
        "filehandle": io.IOBase,
        "filename": str,
        "iterable of node pairs": Iterable[Tuple[Any]],
        "networkx graph constructor": nx.Graph,
        "graph constructor": nx.Graph,
        "constructor": nx.Graph,
        "container": Iterable,
        "data type": Type[Any],
        "dict of dicts": Dict[Any, Dict],
        "class networkx graph": nx.Graph,
        "graph instance": nx.Graph,
        "iterable container of nodes": Iterable[Iterable],
        "graph": nx.Graph,
        "function": FunctionType,
        "four-tuple of numbers": Tuple[Number, Number, Number, Number],
        "sequence": Iterable,
        "list of graphs": List[nx.Graph],
        "container of nodes": Iterable[Any],
        "digraph": nx.DiGraph,
        "node": Type[Any],
        "iterator of pairs of nodes": Iterator[Tuple[Any]],
        "networkx directed graph": nx.DiGraph,
        "networkx digraph": nx.DiGraph,
        "bool": bool,
        "networkx digraph": nx.DiGraph,
        "str in": str,
        "numpy data-type": Type[Any],
        "numpy data type": Type[Any],
        "object to be converted": Type[Any],
        "networkx.graph": nx.Graph,
        "networkx graph": nx.Graph,
        "networkxgraph": nx.Graph,
        "networkx.digraph": nx.DiGraph,
        "class": Type[Any],
        "directed graph": nx.DiGraph,
        "list of ints": List[int],
        "array-like": Iterable,
        "number": Number,
        "list of nodes": List[Any],
        "node label": str,
        "list of lists": List[Iterable[Any]],
        "dict-like": Dict,
        "scalar value": Number,
        "scalar": Number,
        "numpy array": Type[Any],
        "numpy array": Type[Any],
        "dictionary": Dict,
        "dictionary dictionary of dictionaries": Dict[Any, Dict],
        "dictionary of lists": Dict[Any, List],
        "string denoting the requesting metric": str,
        "number of colors to use": Number,
        "list of tuples": List[Tuple],
        "list of three-tuples": List[Tuple[Any]],
        "list of integers": List[int],
        "list of integer pairs": List[Tuple[int, int]],
        "eccentricity dictionary": Dict,
        "boolean function with two arguments": FunctionType,
        "list of sets": List[set],
        "iterable of lists": Iterable[List],
        "positive integer": int,
        "iterator of strings": Iterator[str],
        "numeric": Number,
        "multidigraph": nx.MultiDiGraph,
        "digraph": nx.DiGraph,
        "iterable of strings": Iterable[str],
        "list of list of floats": List[List[float]],
        "networkxdigraph": nx.DiGraph,
        "integer in": int,
        "container of strings": Iterable[str],
        "non-empty set of nodes": Set,
        "container of two-tuples": Iterable[Tuple[Any]],
        "undirected graph": nx.Graph,
        "undirected graph": nx.Graph,
        "digraph-like": nx.DiGraph,
        "3 tuples": Tuple[Any],
        "a set of 2": Set,
        "dictionary of dictionary of integers": Dict[Any, Dict],
        "iterable container": Iterable,
        "a digraph": nx.DiGraph,
        "iterables of nodes": Iterable,
        "tuple of numbers": Tuple[Number],
        "iterable of pairs of nodes": Iterable[Tuple],
        "nodes": Iterable,
        "class str": str,
        "a prime number": Number,
        "networkx graph instance": nx.Graph,
        "tuple of integers": Tuple[int],
        "tuple of node iterables": Tuple[Iterable],
        "generator": Generator,
        "list of nonnegative integers": List[int],
        "the distance of the wanted nodes from source": Number,
        "real": float,
        "list of floats of length m": List[float],
        "list of keys": List,
        "iterator": Iterator,
    }
    tl = typename.lower()
    if tl in type_map:
        return type_map[tl]
    else:
        try:
            return eval(typename)
        except Exception:
            print("***\nCannot interpret: ", typename)
            print("***")

            return Type[Any]


class ParamDesc(Parameter):
    def __init__(self, param, type=[], doc=""):
        super().__init__(
            param.name, param.kind, default=param.default, annotation=param.annotation,
        )
        print(self.name, type)
        self.doc = doc
        self.type = [str_to_type(t) for t in type]

    def __repr__(self):
        return str(self.type)


class ReturnDesc:
    def __init__(self, return_type=None, doc=""):
        super().__init__()
        self.return_type = return_type
        self.doc = doc

    def __repr__(self):
        return str(self.return_type)


class FunctionMetadata(object):
    def __init__(self, name: str, sig: Signature, ast: Dict, doc: str):
        super().__init__()
        self.name = name
        self.signature = self.get_signature(sig, ast)
        self.return_type = ReturnDesc(sig.return_annotation, ast.get(RETURNS, ""))
        self.doc = doc

    def get_signature(self, sig: Signature, ast: Dict) -> Dict[str, ParamDesc]:
        params = {}
        p = ast.get(PARAMETERS, [{}, {}])
        param_types = p[0]
        params_doc = p[1]
        for param_name, param in sig.parameters.items():
            param_doc = params_doc.get(param_name, "")
            param_type = param_types.get(param_name, [])
            param_desc: ParamDesc = ParamDesc(param, param_type, param_doc)
            params[param_name] = param_desc

        return params

    def __repr__(self):
        return f"{self.name}: {self.signature} -> {self.return_type}"


def clean_doc(doc: str) -> str:
    cleaned = ""
    for line in doc.split("\n"):
        line = clean_line(line)
        cleaned += line + "\n"
    return cleaned


def clean_line(line: str):
    line = re.sub(r"\s+", " ", line)
    line = re.sub(r"\s+:", ":", line)
    # line = re.sub(r"\n", "", line)
    line = re.sub(r"^\s+", "", line)
    return line


def get_sections(doc: str) -> Dict:
    lines = doc.split("\n")
    section_pos = []
    for i, line in enumerate(lines):
        if re.match("^\-+", line):
            section_pos.append(i - 1)
    # print(section_pos)
    sections = {}
    for i, pos in enumerate(section_pos):
        section_name = lines[pos]
        start_pos = pos + 2
        if i < len(section_pos) - 1:
            end_pos = section_pos[i + 1]
            section_content = lines[start_pos:end_pos]
        else:
            section_content = lines[start_pos:]
        sections[section_name] = section_content
    return sections


def get_parameters(
    section_content: List[str],
) -> Tuple[Dict[str, List[str]], Dict[str, str]]:

    param_types: Dict[str, List[str]] = {}
    param_docs: Dict[str, str] = {}
    param = None
    for line in section_content:
        match = re.search(r"^(\w+):\s*(.*)$", line)
        if match:
            param = match.group(1)
            # Nx docs may have a "See: NNNNN" section that is not a parameter. It must be removed
            if param != SEE:
                type_str = match.group(2)
                type_str = re.sub("[\.`:\|]", " ", type_str)
                type_str = re.sub(r"\{.*\}", "", type_str)
                type_str = re.sub(r"\[.*\]", "", type_str)
                type_str = re.sub(r"optional", "", type_str)
                type_str = re.sub(r"\s+or(\s+|$)", ",", type_str)
                type_str = clean_line(type_str)
                type_str = re.sub(r"\(.*\)", "", type_str)
                type_str = re.sub(r"default=.*", "", type_str)
                type_str = re.sub(r"\s*,\s*", ",", type_str)
                type_str = re.sub(r",+", ",", type_str).strip()
                type_str = clean_line(type_str)

                param_types[param] = [t for t in type_str.split(",") if t]
                param_docs[param] = ""
        elif param and line:
            if param != SEE:
                param_docs[param] += " " + line

    return (param_types, param_docs)


def parse_nx_doc(doc: str) -> Dict[str, Any]:
    doc = clean_doc(doc)
    # print(doc)
    section = get_sections(doc)
    ast: Dict[str, Any] = {}
    for section_name, content in section.items():
        if section_name == PARAMETERS:
            p = get_parameters(content)
            ast[section_name] = p
        elif section_name == RETURNS:
            ast[section_name] = " ".join(content)
    return ast


def get_member_metadata(m: Tuple):

    if isfunction(m[1]):
        doc = m[1].__doc__
        sig = signature(m[1])
        if doc:
            ast = parse_nx_doc(doc)
        else:
            ast = {}
        return FunctionMetadata(m[0], sig, ast, doc)


if __name__ == "__main__":
    types: Set = set({})
    for m in getmembers(nx):

        md = get_member_metadata(m)
        if md:
            print(md)
            for param, desc in md.signature.items():
                print(desc.name, desc.type)

    # md = get_member_metadata(getmembers(nx)[121])
    # print(md)

    # md = get_member_metadata(("w", nx.watts_strogatz_graph))
    # print(md)
