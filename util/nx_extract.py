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
from doc_mappings import type_map

PARAMETERS = "Parameters"
RETURNS = "Returns"
YIELDS = "Yields"
SEE = "See"


def normalize_typename(typename: str) -> str:
    tl = typename.lower()
    if tl in type_map:
        return type_map[tl]
    else:
        try:
            eval(typename)
            return typename
        except Exception:
            print("#***Cannot", typename)

            return "Any"


def clean_doc(doc: str) -> str:
    cleaned = ""
    for line in re.split("\n|\.", doc):
        line = clean_line(line)
        cleaned += line + "\n"
    return cleaned


def clean_line(line: str):
    line = re.sub(r"\s+", " ", line)
    line = re.sub(r"\s+:", ":", line)
    # line = re.sub(r"\n", "", line)
    line = re.sub(r"^\s+", "", line)
    return line


class ParamDesc(Parameter):
    def __init__(self, param, types=[], doc=""):
        super().__init__(
            param.name, param.kind, default=param.default, annotation=param.annotation,
        )
        # print(self.name, types)
        self.doc = doc
        self.type = list(set(normalize_typename(t) for t in types))

    def __repr__(self):
        return str(self.type)


class RetDesc(object):
    def __init__(self, name, types):
        super().__init__()
        self.name = name
        self.type = list(set(normalize_typename(t) for t in types))


class FunctionMetadata(object):
    def __init__(self, name: str, sig: Signature, ast: Dict, doc: str):
        super().__init__()
        self.name = name
        self.signature = self.get_signature(sig, ast.get(PARAMETERS, [{}, {}]))
        self.return_desc = self.get_ret_signature(sig, ast.get(RETURNS, [{}, {}]))
        self.doc = doc

    def get_ret_signature(
        self, sig: Signature, section: Tuple[Dict, Dict]
    ) -> Dict[str, RetDesc]:
        ret_types = section[0]
        rets = {}
        for ret_name, ret_type in ret_types.items():
            param_desc = RetDesc(ret_name, ret_type)
            rets[ret_name] = param_desc
        return rets

    def get_signature(
        self, sig: Signature, section: Tuple[Dict, Dict]
    ) -> Dict[str, ParamDesc]:
        params = {}
        param_types = section[0]
        param_docs = section[1]
        for param_name, param in sig.parameters.items():
            param_doc = param_docs.get(param_name, "")
            param_type = param_types.get(param_name, [])
            # print("--", param_type)
            param_desc = ParamDesc(param, param_type, param_doc)
            params[param_name] = param_desc
        # print("-- ", params)
        return params

    def __repr__(self):
        return f"{self.name}: {self.signature} -> {self.return_type}"


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
    key_val_pattern = r"^(\w+)\s*:\s*(.*)$"

    for line in section_content:
        match = re.search(key_val_pattern, line)
        if match:
            param = match.group(1)
            # Nx docs may have a "See: NNNNN" section that is not a parameter. It must be removed
            if param != SEE:
                type_str = match.group(2)
                param_types[param] = extract_type_from_str(type_str)
                param_docs[param] = ""
        elif param and line:
            if param != SEE:
                param_types[param] = extract_type_from_str(line)
                param_docs[param] += " " + line

    return (param_types, param_docs)


def extract_type_from_str(type_str):
    # type_str = re.sub("[\.`:\|]", " ", type_str)
    type_str = re.sub("[`:\|]", " ", type_str)
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

    return [t for t in type_str.split(",") if t]


def parse_nx_doc(doc: str) -> Dict[str, Any]:
    doc = clean_doc(doc)
    # print(doc)
    section = get_sections(doc)
    ast: Dict[str, Any] = {}
    for section_name, content in section.items():
        if section_name == PARAMETERS:
            ast[section_name] = get_parameters(content)
        elif section_name == RETURNS or section_name == YIELDS:
            ast[section_name] = get_parameters(content)

    return ast


def get_member_metadata(m: Tuple) -> Optional[FunctionMetadata]:

    if isfunction(m[1]):
        doc = m[1].__doc__
        sig = signature(m[1])
        if doc:
            ast = parse_nx_doc(doc)
        else:
            ast = {}
        return FunctionMetadata(m[0], sig, ast, doc)
    return None


if __name__ == "__main__":
    types: Set = set({})
    for m in getmembers(nx):

        md = get_member_metadata(m)
        if md:
            # print(md)
            for param, desc in md.signature.items():
                print(desc.type)

